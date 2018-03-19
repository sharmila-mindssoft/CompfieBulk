var STATUTORY_MAPPING_REPORT_DATA;
var SYSTEM_REJECTED = "COMPFIE";
var ON_CURRENT_PAGE = 1;
var SNO = 0;
var TOTAL_RECORD = 0;
var ITEMS_PER_PAGE = $('#items_per_page');
var SHOW_BTN = $('#show');
var EXPORT_BTN = $('#export');
var PAGINATION_VIEW = $('.pagination-view');
var PAGINATION = $('#pagination-rpt');
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
var SM_MAPPING = null;
var ALL_USER_INFO;
var USER_DETAILS;
/**** User Level Category ***********/
var KM_USER_CATEGORY = 3;
var KE_USER_CATEGORY = 4;
var TM_USER_CATEGORY = 5;
var TM_USER_CATEGORY = 6;
var DM__USER_CATEGORY = 7;
var DE_USER_CATEGORY = 8;
// Creating SM_Report Class
function SM_Report() {}
// To get the corresponding value
SM_Report.prototype.getValue = function(field_name, f_id) {
    if (field_name == "from_date") {
        f_date = FROM_DATE.val().trim();
        return f_date;
    } else if (field_name == "to_date") {
        f_date = TO_DATE.val().trim();
        return f_date;
    }
};
// Fields Manadory validation
SM_Report.prototype.validateMandatory = function() {
    is_valid = true;
    if ($('#country option:selected').text() == "") {
        displayMessage(message.country_required);
        is_valid = false;
    } else if ($('#domain option:selected').text() == "") {
        displayMessage(message.domain_required);
        is_valid = false;
    } else if (this.getValue("from_date") == "") {
        displayMessage(message.fromdate_required);
        is_valid = false;
    } else if (this.getValue("to_date") == "") {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};
//get statutory mapping bulk report filter details from api
function getStatutoryMappings() {
    function onSuccess(data) {
        country_list = data.countries;
        domain_list = data.domains;
        ALL_USER_INFO = data.user_details;
        USER_DETAILS = data.user_details[0];
        DOMAIN_IDS = USER_DETAILS.country_wise_domain;
        EMP_CODE = USER_DETAILS.employee_code;
        EMP_NAME = USER_DETAILS.employee_name;
        //Load Countries MultiSelectBox
        for (var c in country_list) {
            var option = $('<option></option>');
            option.val(country_list[c].country_id);
            option.text(country_list[c].country_name);
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
    var country_name, domain_name, csv_name, tbl_no_of_tasks, uploaded_by;
    var uploaded_on, total_rejected_records, rejected_on, rejected_by;
    var approved_on, approved_by, reason_for_rejection, total_approve_records;
    var rejected_reason, approved_rejected_on, approved_rejected_by;
    var approved_rejected_tasks;
    var is_null = true;
    var last_act_name = '';
    var entity;
    var table_row;
    SHOW_FROM = SNO + 1;
    for (var entity in data) {
        is_null = false;
        SNO = parseInt(SNO) + 1;
        country_name = data[entity].country_name;
        domain_name = data[entity].domain_name;
        csv_name = data[entity].csv_name_text;
        tbl_no_of_tasks = data[entity].total_records;
        uploaded_by = data[entity].uploaded_by;
        uploaded_on = data[entity].uploaded_on;
        total_rejected_records = data[entity].total_rejected_records;
        rejected_on = data[entity].rejected_on;
        rejected_by = data[entity].rejected_by;
        approved_on = data[entity].approved_on;
        approved_by = data[entity].approved_by;
        reason_for_rejection = data[entity].is_fully_rejected;
        total_approve_records = data[entity].total_approve_records;
        rejected_reason = data[entity].rejected_reason;
        approved_rejected_on = '';
        approved_rejected_by = '';
        approved_rejected_tasks = '-';
        $(ALL_USER_INFO).each(function(key, value) {
            if (parseInt(uploaded_by) == value["user_id"]) {
                EMP_CODE = value["employee_code"];
                EMP_NAME = value["employee_name"];
                uploaded_by = EMP_CODE + " - " + EMP_NAME;
            } else if (parseInt(rejected_by) == value["user_id"]) {
                EMP_CODE = value["employee_code"];
                EMP_NAME = value["employee_name"];
                rejected_by = EMP_CODE + " - " + EMP_NAME;
            } else if (parseInt(approved_by) == value["user_id"]) {
                EMP_CODE = value["employee_code"];
                EMP_NAME = value["employee_name"];
                approved_by = EMP_CODE + " - " + EMP_NAME;
            }
        });
        if (parseInt(reason_for_rejection) == 1) {
            reason_for_rejection = rejected_reason;
        } else {
            reason_for_rejection = "";
            approved_rejected_tasks = total_approve_records;
            approved_rejected_tasks += " / ";
            approved_rejected_tasks += total_rejected_records;
        }
        if (String(approved_on) != "null") {
            approved_rejected_on = approved_on;
            approved_rejected_by = approved_by;
        }
        if (String(rejected_on) != "null") {
            approved_rejected_on = rejected_on;
            approved_rejected_by = rejected_by;
        }
        table_row = $('#act_templates .table-act-list .table-row-act-list');
        var tr_clone = table_row.clone();
        $('.tbl-sno', tr_clone).text(SNO);
        $('.tbl-country', tr_clone).text(country_name);
        $('.tbl-domain', tr_clone).text(domain_name);
        $('.tbl-uploaded-file-name', tr_clone).text(csv_name);
        $(".tbl-uploaded-by", tr_clone).text(uploaded_by);
        $('.tbl-uploaded-on', tr_clone).text(uploaded_on);
        $('.tbl-no-of-tasks', tr_clone).text(tbl_no_of_tasks);
        $('.tbl-approved-rejected-tasks', tr_clone).text(approved_rejected_tasks);
        $('.tbl-approved-rejected-on', tr_clone).text(approved_rejected_on);
        $('.tbl-approved-rejected-by', tr_clone).text(approved_rejected_by);
        $('.tbl-reason-for-rejection', tr_clone).text(reason_for_rejection);
        $('#datatable_responsive .tbody-compliance').append(tr_clone);
    }
    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(SHOW_FROM, SNO, TOTAL_RECORD);
    }
    hideLoader();
}
// get statutory mapping report data from api
function processSubmit() {
    displayLoader();
    var country = COUNTRY.val();
    var domain = DOMAIN.val();
    var from_date = $('#from_date').val();
    var to_date = $('#to_date').val();
    var selected_ke = [];
    var selected_country_id = [];
    var selected_domain_id = [];
    var split_domain_name;
    /* multiple COUNTRY selection */
    $.each(country, function(key, value) {
        selected_country_id.push(parseInt(value));
    });
    /* multiple DOMAIN selection */
    $.each(domain, function(key, value) {
        split_domain_name = value.split("-");
        selected_domain_id.push(parseInt(split_domain_name[1]));
    });
    if ($('#kename-kmanager').val() == null) {
        selected_ke = KNOWLEDGE_EXECUTIVES;
    } else {
        $('#kename-kmanager > option:selected').each(function() {
            selected_ke.push(parseInt(this.value));
        });
    }
    _page_limit = parseInt(ITEMS_PER_PAGE.val());
    if (ON_CURRENT_PAGE == 1) {
        SNO = 0
    } else {
        SNO = (ON_CURRENT_PAGE - 1) * _page_limit;
    }
    filterdata = {
        "c_ids": selected_country_id,
        "d_ids": selected_domain_id,
        "from_date": from_date,
        "to_date": to_date,
        "r_count": SNO,
        "p_count": _page_limit,
        "child_ids": selected_ke,
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
    bu.getStatutoryMappingsBulkReportData(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
    //temp_act = act;
    //}
}
/******** Load Domain Lists *********/
function loadDomains() {
    DOMAIN.empty();
    if (COUNTRY.val() != null) {
        var select_countries = COUNTRY.val().map(Number);
        var str = '';
        $.each(country_list, function(key, value) {
            var cId = value.country_id;
            if ($.inArray(cId, select_countries) >= 0) {
                var flag = true;
                $.each(domain_list, function(key1, v) {
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
                if (flag == false) str += '</optgroup>'
            }
        });
        DOMAIN.append(str);
        DOMAIN.multiselect('rebuild');
    }
}
/****** Pagination ***********/
function showPagePan(SHOW_FROM, showTo, total) {
    var showText = 'Showing ' + SHOW_FROM + ' to ' + showTo + ' of ';
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
    perPage = parseInt(ITEMS_PER_PAGE.val());
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
        perPage = parseInt($(this).val());
        SNO = 0;
        ON_CURRENT_PAGE = 1;
        createPageView(TOTAL_RECORD);
        processSubmit();
    });
    SHOW_BTN.click(function() {
        is_valid = SM_MAPPING.validateMandatory();
        if (is_valid == true) {
            SM_MAPPING._ON_CURRENT_PAGE = 1;
            SM_MAPPING._total_record = 0;
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
        is_valid = SM_MAPPING.validateMandatory();
        if (is_valid == true) {
            CSV = true;
            SM_MAPPING.exportData();
        }
    });
}
/****** Get Current User Employee Name & Code ***********/
function loadCurrentUserDetails() {
    var user = mirror.getUserInfo();
    var logged_user_id = 0;
    var knowledge_name;
    var knowledge_user_details = {};
    $.each(ALL_USER_INFO, function(key, value) {
        if (user.user_id == value["user_id"]) {
            USER_CATEGORY_ID = value["user_category_id"];
            logged_user_id = value["user_id"];
        }
    });
    if (USER_CATEGORY_ID == KE_USER_CATEGORY) {
        // KE-Name  : Knowledge-Executive
        knowledge_name = user.employee_code + " - " +
            user.employee_name;
        $('.active-knowledge-executive').attr('style', 'display:block');
        $('#knowledge_name').text(knowledge_name);
        knowledge_user_details = {
            /*"user_name":knowledge_name,*/
            "user_id": user.user_id
        }
        ALLUSERS.push(knowledge_user_details);
        KNOWLEDGE_EXECUTIVES.push(user.user_id);
    } else if (USER_CATEGORY_ID == KM_USER_CATEGORY && USER_CATEGORY_ID != KE_USER_CATEGORY &&
        logged_user_id > 0) {
        // KE-Name  : Knowledge-Manager
        getUserMappingsList(logged_user_id);
    }
}
//get statutory mapping bulk report filter details from api
function getUserMappingsList(logged_user_id) {
    $('.form-group-kename-kmanager').attr("style", "display:block !important");
    $('#kename_kmanager').multiselect('rebuild');

    function onSuccess(logged_user_id, data) {
        console.log("logged_user_id->" + logged_user_id);
        var userMappingData = data;
        var d;
        $.each(userMappingData.user_mappings, function(key, value) {
            if (logged_user_id == value.parent_user_id) {
                if (jQuery.inArray(value.child_user_id, KNOWLEDGE_EXECUTIVES) == -1) {
                    console.log("inif")
                    KNOWLEDGE_EXECUTIVES.push(value.child_user_id);
                    childUsersDetails(
                        ALL_USER_INFO,
                        logged_user_id,
                        value.child_user_id);
                }
            }
        });
    }

    function childUsersDetails(ALL_USER_INFO, parent_user_id, child_user_id) {
        var knowledge_user_details = {}
        $.each(ALL_USER_INFO, function(key, value) {
            if (child_user_id == value["user_id"] && value["is_active"] == true) {
                var option = $('<option></option>');
                option.val(value["user_id"]);
                option.text(value["employee_code"] + " - " + value["employee_name"]);
                $('#kename_kmanager').append(option);
                knowledge_name = value["employee_code"] + " - " +
                    value["employee_name"].toUpperCase();
                knowledge_user_details = {
                    "name": knowledge_name,
                    "user_id": value["user_id"]
                }
                ALLUSERS.push(knowledge_user_details);
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
            onSuccess(logged_user_id, response);
        } else {
            onFailure(error);
        }
    });
}

function Statutory_mapping_bulk_report_page() {}
// Instance Creation of the page class
SM_MAPPING = new SM_Report();
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
//To export data
SM_Report.prototype.exportData = function() {
    var country = COUNTRY.val();
    var domain = DOMAIN.val();
    var fromDate = $('#from_date').val();
    var toDate = $('#to_date').val();
    var selected_country_id = [];
    var selected_domain_id = [];
    var split_domain_name;
    var downloadCSV = true;
    var selected_ke = [];
    // multiple COUNTRY selection in to generate array
    $.each(country, function(key, value) {
        selected_country_id.push(parseInt(value));
    });
    var countryNames = $("#country option:selected").map(function() {
        return $(this).text();
    }).get().join(',');
    console.log("countryNames-> " + countryNames);
    // multiple DOMAIN selection generate as a array
    $.each(domain, function(key, value) {
        split_domain_name = value.split("-");
        selected_domain_id.push(parseInt(split_domain_name[1]));
    });
    var domainNames = $("#domain option:selected").map(function() {
        return $(this).text();
    }).get().join(',');
    console.log("domainNames-> " + domainNames);
    if ($('#kename-kmanager').val() == null) {
        selected_ke = KNOWLEDGE_EXECUTIVES;
    } else {
        $('#kename-kmanager > option:selected').each(function() {
            console.log(this.value);
            selected_ke.push(parseInt(this.value));
        });
    }
    filterdata = {
        "c_ids": selected_country_id,
        "c_names": countryNames,
        "d_ids": selected_domain_id,
        "d_names": domainNames,
        "child_ids": selected_ke,
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