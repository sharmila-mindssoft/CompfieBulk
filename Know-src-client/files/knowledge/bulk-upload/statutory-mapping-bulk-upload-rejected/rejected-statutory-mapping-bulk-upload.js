var COUNTRIES_LIST = [];
var DOMAIN_LIST = [];
var ALL_USER_INFO = [];
var USER_DETAILS;
var DOMAIN_IDS;
var EMP_CODE;
var EMP_NAME;
var REJECTED_STATUTORY_DATA;
var COUNTRY_VAL = $('#countryval');
var COUNTRY = $('#country');
var DOMAIN = $('#domain');
var DOMAIN_VAL = $('#domainval');
var AC_COUNTRY = $('#ac-country');
var AC_DOMAIN = $('#ac-domain');
var SHOW_BTN = $('#show');
var EXPORT_CSV = $('.export-csv');
var REPORT_VIEW = $('.grid-table-rpt');
var PASSWORD_SUBMIT_BTN = $('#password-submit');
var CURRENT_PASSWORD = $('#current-password');
var REMOVE_STATUTORY_CSV_ID;

// Creating New Class
var rejStatuMapping = new RejectedStatutoryMappingBulk();

// Handle All Page Controls like Button submit
function pageControls() {
    //load group form list in autocomplete text box
    COUNTRY_VAL.keyup(function(e) {
        var textVal = $(this).val();
        var cgList = [];
        resetfilter("domain");
        var i = 0;
        for (i = 0; i < COUNTRIES_LIST.length; i++) {
            if (COUNTRIES_LIST[i].is_active == true) {
                var occur = -1;
                var j = 0;
                for (j = 0; j < cgList.length; j++) {
                    if (cgList[j].country_id == COUNTRIES_LIST[i].country_id) {
                        occur = 1;
                        break;
                    }
                }
                if (occur < 0) {
                    cgList.push({
                        "country_id": COUNTRIES_LIST[i].country_id,
                        "country_name": COUNTRIES_LIST[i].country_name,
                        "is_active": true
                    });
                }

            }
        }
        commonAutoComplete(
            e, AC_COUNTRY, COUNTRY, textVal,
            cgList, "country_name", "country_id",
            function(val) {
                onAutoCompleteSuccess(COUNTRY_VAL, COUNTRY, val);
            });
    });


    //load legalentity form list in autocomplete text box
    DOMAIN_VAL.keyup(function(e) {
        resetfilter('');
        var textVal = $(this).val();
        var dList = [];
        var ctryId = COUNTRY.val();
        var c_id;
        if (COUNTRY.val() > 0) {
            var conditionFields = [];
            var conditionValues = [];
            if (COUNTRY.val() != '') {
                conditionFields.push("country_id");
                conditionValues.push(COUNTRY.val());
            }
            var i = 0;
            for (i = 0; i < COUNTRIES_LIST.length; i++) {
                if ((COUNTRIES_LIST[i].country_id == ctryId)) {
                    for (var j = 0; j < DOMAIN_LIST.length; j++) {
                        c_id = COUNTRIES_LIST[i].country_id
                        if ($.inArray(c_id, DOMAIN_LIST[j].country_ids) >= 0) {
                            dList.push({
                                "domain_id": DOMAIN_LIST[j].domain_id,
                                "domain_name": DOMAIN_LIST[j].domain_name,
                                "is_active": true
                            });
                        }
                    }
                }
            }
            commonAutoComplete(
                e, AC_DOMAIN, DOMAIN, textVal,
                dList, "domain_name", "domain_id",
                function(val) {
                    onAutoCompleteSuccess(DOMAIN_VAL, DOMAIN, val);
                });
        }

    });

    SHOW_BTN.click(function() {
        isValid = rejStatuMapping.validateMandatory();
        if (isValid == true) {
            processSubmit();
        }
    });
}

//
function resetfilter(evt) {
    if (evt == "domain") {
        DOMAIN_VAL.val('');
        DOMAIN.val('');
    }
    $('.tbody-usermappingdetails-list').empty();
    $('.grid-table-rpt').hide();
    $('.details').hide();
}

function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    var currentId = idElement[0].id;
    if (currentId == 'country') {} else if (currentId == 'domainid') {}
}

// get statutory mapping report data from api
function processSubmit() {
    var countryID = parseInt(COUNTRY.val());
    var domainID = parseInt(DOMAIN.val());

    displayLoader();
    filterdata = {
        "c_id": countryID,
        "d_id": domainID,
    };

    function onSuccess(data) {
        $('.details').show();
        REJECTED_STATUTORY_DATA = data.rejected_data;
        if (REJECTED_STATUTORY_DATA.length == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates ' +
                '.table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            REPORT_VIEW.show();
            hideLoader();
        } else {
            REPORT_VIEW.show();
            loadCountwiseResult(REJECTED_STATUTORY_DATA);
            hideLoader();
        }
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    bu.getRejectedSMBulkData(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

//Display statutory mapping details accoring to count
function loadCountwiseResult(data) {
    var sno = 0;
    var csvId;
    var csvName;
    var totalNoofTasks;
    var rejectedOn;
    var reasonForRejection;
    var statutoryAction;
    var rejectedBy;
    var declinedCount;
    var fileDownloadCount;
    var downloadRejectedFiles;
    var isFullyRejected;

    $('.tbody-compliance').empty();
    for (var entity in data) {
        sno = parseInt(sno) + 1;
        csvId = data[entity].csv_id;
        csvName = data[entity].csv_name_text;
        totalNoofTasks = data[entity].total_records;
        rejectedOn = data[entity].rejected_on;
        approvedOn = data[entity].approved_on;
        isFullyRejected = data[entity].is_fully_rejected;
        rejectedReason = data[entity].rejected_reason;
        statutoryAction = data[entity].statutory_action;
        fileDownloadCount = data[entity].file_download_count;
        declinedCount = '-';
        reasonForRejection = '';

        if (parseInt(isFullyRejected) == 1) {
            removeAction = '';
            reasonForRejection = rejectedReason;
            $(ALL_USER_INFO).each(function(key, value) {
                if (parseInt(data[entity].rejected_by) == value["user_id"]) {
                    EMP_CODE = value["employee_code"];
                    EMP_NAME = value["employee_name"];
                    rejectedBy = EMP_CODE + " - " + EMP_NAME;
                }
            });
        } else if (parseInt(statutoryAction) == 3) {
            rejectedBy = SYSTEM_REJECTED_BY;
            declinedCount = data[entity].declined_count;
            reasonForRejection = '';
            rejectedOn = approvedOn;
        }

        var tr = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tr.clone();

        $('.tbl_sno', clone1).text(sno);
        $('.tbl_upload_filename', clone1).text(csvName);
        $(".tbl_rejected_on", clone1).text(rejectedOn);
        $('.tbl_rejected_by', clone1).text(rejectedBy);
        $('.tbl_no_of_tasks', clone1).text(totalNoofTasks);
        $('.tbl_declined_count', clone1).text(declinedCount);
        $('.tbl_reason_for_rejection', clone1).text(reasonForRejection);

        $('.tbl_remove .remove_a', clone1).attr({
            'id': "delete_action_" + csvId,
            'data-csv-id': csvId,
            onClick: "confirmAlert(this)",
        });
        /***** Rejected File Downloads ********/
        if (parseInt(fileDownloadCount) < parseInt(REJECTED_FILE_DOWNLOADCOUNT)) {
            $('.tbl_rejected_file .rejected_i_cls', clone1).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)"
            });
            $('.tbl_rejected_file .rejected_div_cls', clone1).attr({
                'id': "download_files_" + csvId
            });
            $('.tbl_rejected_file .rejected_div_cls .rej_excel, .rej_csv, ' +
                '.rej_ods, .rej_text', clone1).attr({
                onclick: "downloadClick(" + csvId + ",this)"
            });
        }
        else{
            $('.tbl_rejected_file .rejected_i_cls', clone1).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)",
            });
            $('.tbl_rejected_file .rejected_i_cls', clone1)
            .addClass("default-display-none");
        }
        if (parseInt(fileDownloadCount) < 1){
            $('.tbl_remove .remove_a', clone1).addClass("default-display-none");
        }
        $('#datatable-responsive .tbody-compliance').append(clone1);
    }
    hideLoader();
}

function RejectedStatutoryMappingBulk() {}
// Fields Manadory validation
RejectedStatutoryMappingBulk.prototype.validateMandatory = function() {
    var isValid = true;
    if (COUNTRY.val().trim().length == 0) {
        displayMessage(message.country_required);
        isValid = false;
    } else if (DOMAIN.val().trim().length == 0) {
        displayMessage(message.domain_required);
        isValid = false;
    }
    return isValid;
};

//load all the filters
function initialize() {
    function onSuccess(data) {
        COUNTRIES_LIST = data.countries;
        DOMAIN_LIST = data.domains;
        ALL_USER_INFO = data.user_details;
        USER_DETAILS = data.user_details[0];
        DOMAIN_IDS = USER_DETAILS.country_wise_domain;
        EMP_CODE = USER_DETAILS.employee_code;
        EMP_NAME = USER_DETAILS.employee_name;
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getAdminUserList(function(error, response) {
        if (error == null) {
            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}

//validate password
function validateAuthentication() {
    var password = CURRENT_PASSWORD.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CURRENT_PASSWORD.focus();
        return false;
    } else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }
    displayLoader();
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            hideLoader();
            isAuthenticate = true;
            Custombox.close();
        } else {
            hideLoader();
            if (error == 'InvalidPassword') {
                displayMessage(message.invalid_password);
            }
        }
    });
}

PASSWORD_SUBMIT_BTN.click(function() {
    validateAuthentication();
});

function confirmAlert(event) {
    var countryId = COUNTRY.val();
    var domainId = DOMAIN.val();
    swal({
        title: "Are you sure",
        text: "You want to permanently delete the file?",
        type: "success",
        showCancelButton: true,
        confirmButtonClass: 'btn-success waves-effect waves-light',
        confirmButtonText: 'Yes'
    }, function(isConfirm) {
        if (isConfirm) {
            Custombox.open({
                target: '#custom-modal-approve',
                effect: 'contentscale',
                complete: function() {
                    if (CURRENT_PASSWORD != null) {
                                    CURRENT_PASSWORD.focus();
                                    CURRENT_PASSWORD.val('');
                                }
                    CURRENT_PASSWORD.focus();
                    isAuthenticate = false;
                    COUNTRY.val(countryId);
                    DOMAIN.val(domainId);
                },
                close: function() {
                    COUNTRY.val(countryId);
                    DOMAIN.val(domainId);
                    if (isAuthenticate) {
                        REMOVE_STATUTORY_CSV_ID = $(event).attr("data-csv-id");
                        RemoveStatutoryCsv(REMOVE_STATUTORY_CSV_ID, countryId,
                            domainId);
                    }
                }
            });
        }
    })
}

// Remove Button functionality
function RemoveStatutoryCsv(REMOVE_STATUTORY_CSV_ID, countryId, domainId) {
    displayLoader();

    function onSuccess(data) {
        $('.details').show();
        COUNTRY.val(countryId);
        DOMAIN.val(domainId);

        $('.details').show();
        $(this).show();

        REJECTED_STATUTORY_DATA = data.rejected_data;
        if (REJECTED_STATUTORY_DATA.length == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates '+
                '.table-nocompliances-list ' +
                '.table-row');
            var clone4 = tableRow4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            REPORT_VIEW.show();
            hideLoader();
        } else {
            hideLoader();
            REPORT_VIEW.show();
            loadCountwiseResult(REJECTED_STATUTORY_DATA);
        }
        displaySuccessMessage(message.record_deleted);

    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    filterdata = {
        "d_id": parseInt(domainId),
        "csv_id": parseInt(REMOVE_STATUTORY_CSV_ID),
        "c_id": parseInt(countryId)
    };

    bu.deleteRejectedSMByCsvID(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response)
        } else {

            onFailure(error);
        }
    });
    hideLoader();
}

// Download Click functionality
function downloadClick(CSV_ID, event) {
    var cId = COUNTRY.val();
    var dId = DOMAIN.val();
    var downloadFileFormat = $(event).attr("data-format");

    displayLoader();

    function onSuccess(data) {
        var updatedCount;
        var dataCsvId;
        var downloadCount;
        var eventId = "download_files_";
        //delete_action_
        updatedCount = data.updated_count;

        dataCsvId = updatedCount[0].csv_id;
        downloadCount = updatedCount[0].download_count;
        if (parseInt(downloadCount) == 1) {
            eventId = eventId + dataCsvId;
            document.getElementById(eventId).classList.toggle("show");
            $("#delete_action_" + dataCsvId).attr("style", "display:block");
        }
        else if (
            parseInt(downloadCount) >= parseInt(REJECTED_FILE_DOWNLOADCOUNT)) {
            eventId = eventId + dataCsvId;
            document.getElementById(eventId).classList.toggle("show");
            $("#delete_action_" + dataCsvId).attr("style", "display:block");
            $("#download_files_" + dataCsvId).remove();
            $("#download_icon_" + dataCsvId).remove();
        }
        displaySuccessMessage(message.download_files);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    //csvId
    filterdata = {
        "csv_id": parseInt(CSV_ID)
    };

    var requestDownloadData = {
        "csv_id": parseInt(CSV_ID),
        "c_id": parseInt(cId),
        "d_id": parseInt(dId),
        "download_format": downloadFileFormat
    };
    bu.setDownloadClickCount(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response);
            requestDownload(requestDownloadData, downloadFileFormat);
            displayLoader();
        } else {
            onFailure(error);
        }
    });
    hideLoader();
    return false;
}

// Download Request
function requestDownload(requestDownloadData, downloadFileFormat) {
    bu.downloadRejectedSMReportData(requestDownloadData,
        function(error, response) {
        if (error == null) {
            if (downloadFileFormat == "csv") {
                $(location).attr('href', response.csv_link);
                hideLoader();
                return false;
            } else if (downloadFileFormat == "excel") {
                $(location).attr('href', response.xlsx_link);
                hideLoader();
                return false;
            } else if (downloadFileFormat == "text") {
                    $.get(response.txt_link, function(data){
                        url = response.txt_link
                        txt_file_name = url.substring(url.lastIndexOf('/')+1)
                        download(txt_file_name, "text/plain", data);
                    },
                    'text');
                    hideLoader();
            } else if (downloadFileFormat == "ods") {
                $(location).attr('href', response.ods_link);
                hideLoader();
                return false;
            }

        } else {
            hideLoader();
        }

    });
}
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
// File Download
function downloadFile(filePath) {
    var link = document.createElement('a');
    link.href = filePath;
    link.download = filePath.substr(filePath.lastIndexOf('/') + 1);
    link.click();
}

/* DownloadFileOptionList - Excel,CSV,ODS,Text  */
function rejectedFiles(event) {
    var eventId = $(event).attr("data-id");
    eventId = "download_files_" + eventId;
    document.getElementById(eventId).classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
$(function() {
    bu.getLoadConstants();
    $('.grid-table-rpt').hide();
    initialize();
    pageControls();
});