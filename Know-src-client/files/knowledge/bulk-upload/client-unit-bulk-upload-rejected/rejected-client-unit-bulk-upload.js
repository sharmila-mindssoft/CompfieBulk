var GROUP_NAME = $('#groupval');
var GROUP_ID = $('#group');
var AC_GROUP = $('#ac_group');
var SHOW_BTN = $('#show');
var REPORT_VIEW = $('.grid-table-rpt');
var PASSWORD_SUBMIT_BUTTON = $('#password_submit');
var CURRENT_PASWORD = $('#current_password');
var REMOVE_UNIT_CSV_ID = '';
var ALL_USER_INFO = '';
var CLIENT_LIST = '';

var rejClientUnit = new rejectedClientUnitBulk();
function rejectedClientUnitBulk() {}

// Handle All Page Controls 
function pageControls() {
    //load group form list in autocomplete text box
    GROUP_NAME.keyup(function(e) {
        var textVal = $(this).val();
        commonAutoComplete(
            e, AC_GROUP, GROUP_ID, textVal,
            CLIENT_LIST, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GROUP_NAME, GROUP_ID, val);
            });
        resetFilter();
    });

    SHOW_BTN.click(function() {
        isValid = rejClientUnit.validateMandatory();
        if (isValid == true) {
            processSubmit();
        }
    });
}

function onAutoCompleteSuccess(valueElement, idElement, val) {
    var currentId = 0;
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    currentId = idElement[0].id;
}

// Get Client Unit Rejected report data from api once click show button
function processSubmit() {
    var groupId = parseInt(GROUP_ID.val());
    var filterData = {};
    displayLoader();
    filterData = {
        "bu_client_id": groupId
    };
    function onSuccess(data) {
        var tableRow4 = '', clone4 = '';
        $('.details').show();
        rejClientUnitData = data.rejected_unit_data;
        if (rejClientUnitData.length == 0) {
            $('.tbody-compliance').empty();
            tableRow4 = $('#nocompliance_templates ' +
                '.table-nocompliances-list .table-row');
            clone4 = tableRow4.clone();
            $('.tbl-norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            REPORT_VIEW.show();
            hideLoader();
        } else {
            hideLoader();
            REPORT_VIEW.show();
            loadCountwiseResult(rejClientUnitData);
        }
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    bu.getClientUnitRejectedData(filterData, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

// Display Rejected Client Unit details accoring to count
function loadCountwiseResult(data) {
    var sno = 0;
    var csvId = 0;
    var totalNoOfTasks = 0;
    var csvName = '';
    var rejectedOn = '', rejectedBy = '';
    var reasonForRejection = '';
    var statutoryAction = '';    
    var declinedCount = '';
    var fileDownloadCount = '';
    var isFullyRejected = '';
    var deleteStatus = '', approvedOn = '';
    var entity = '', tblRow1 = '', clone1 = '';

    $('.tbody-compliance').empty();
    for (entity in data) {
        deleteStatus = '';
        sno = parseInt(sno) + 1;
        csvId = data[entity].csv_id;
        csvName = data[entity].csv_name;
        totalNoOfTasks = data[entity].total_records;
        rejectedOn = data[entity].rejected_on;
        approvedOn = data[entity].approved_on;
        rejectedBy = data[entity].rejected_by;
        isFullyRejected = data[entity].is_fully_rejected;
        statutoryAction = data[entity].statutory_action;
        fileDownloadCount = data[entity].file_download_count;
        rejectedReason = data[entity].rejected_reason;
        declinedCount = data[entity].declined_count;
        rejectedFileName = data[entity].rejected_file;
        reasonForRejection = '';

        if (parseInt(isFullyRejected) == 1) {
            removeHrefTag = '';
            reasonForRejection = rejectedReason;
            $(ALL_USER_INFO).each(function(key, value) {
                if (parseInt(rejectedBy) == value["user_id"]) {
                    EmpCode = value["employee_code"];
                    EmpName = value["employee_name"];
                    rejectedBy = EmpCode + " - " + EmpName;
                }
            });
        }
        else if (parseInt(statutoryAction) == 3) {
            rejectedBy = SYSTEM_REJECTED_BY;
            rejectedOn = approvedOn;
            reasonForRejection = '';
        }
        tblRow1 = $('#act_templates .table-act-list .table-row-act-list');
        clone1 = tblRow1.clone();
        $('.tbl-sno', clone1).text(sno);
        $('.tbl-upload-filename', clone1).text(csvName);
        $(".tbl-rejected-on", clone1).text(rejectedOn);
        $('.tbl-rejected-by', clone1).text(rejectedBy);
        $('.tbl-no-of-tasks', clone1).text(totalNoOfTasks);
        $('.tbl-declined-count', clone1).text(declinedCount);
        $('.tbl-reason-for-rejection', clone1).text(reasonForRejection);
        $('.tbl-remove .remove-a', clone1).attr({
            'id': "delete_action_" + csvId,
            'data-csv-id': csvId,
            onClick: "confirm_alert(this)",
        });
        /***** Rejected File Downloads ********/
        if (parseInt(fileDownloadCount) < REJECTED_FILE_DOWNLOADCOUNT) {
            $('.tbl-rejected-file .rejected-i-cls', clone1).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)"
            });
            $('.tbl-rejected-file .rejected-div-cls', clone1).attr({
                'id': "download_files_" + csvId
            });
            $('.tbl-rejected-file .rejected-div-cls .rej-excel, .rej-csv, ' +
                '.rej-ods, .rej-text', clone1).attr({
                onclick: "downloadClick(" + csvId + ",this)"
            });
        }
        else{
            $('.tbl-rejected-file .rejected-i-cls', clone1).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)",
            });
            $('.tbl-rejected-file .rejected-i-cls', clone1)
            .addClass("default-display-none");
        }
        if (parseInt(fileDownloadCount) < 1){
            $('.tbl-remove .remove-a', clone1).addClass("default-display-none");
        }
        $('#datatable_responsive .tbody-compliance').append(clone1);
    }
    hideLoader();
}

// Fields Manadory validation
rejectedClientUnitBulk.prototype.validateMandatory = function() {
    isValid = true;
    if (GROUP_NAME.val().trim().length == 0) {
        displayMessage(message.client_group_required);
        isValid = false;
    }
    return isValid;
};

//Initialize the page load user list
function initialize() {
    function onSuccess(data) {
        CLIENT_LIST = data.client_group_list;
        allUserInfo();        
        hideLoader();
    }
    
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    bu.getClientGroupsList(function(error, response) {
        if (error == null) {
            onSuccess(response);
        }
        else {
            onFailure(error);
        }
    });
}

// Get logged user details from api
function allUserInfo() {
    function onSuccess(data) {
        ALL_USER_INFO = data.user_details;
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getAdminUserList(function(error, response) {
        if (error == null) {
            onSuccess(response);
        }
        else {
            onFailure(error);
        }
    });
}

//validate password
function validateAuthentication() {
    var password = CURRENT_PASWORD.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CURRENT_PASWORD.focus();
        return false;
    }
    else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }
    displayLoader();
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            hideLoader();
            isAuthenticate = true;
            Custombox.close();
            CURRENT_PASWORD.val('');
        }
        else {
            hideLoader();
            if (error == 'InvalidPassword') {
                displayMessage(message.invalid_password);
            }
        }
    });
}

PASSWORD_SUBMIT_BUTTON.click(function() {
    validateAuthentication();
});

// popup confirmation box, this appear when delete clientunit
function confirm_alert(event) {
    var groupId = GROUP_ID.val();
    CURRENT_PASWORD.val('');
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
                target: '#custom_modal_approve',
                effect: 'contentscale',
                complete: function() {
                    CURRENT_PASWORD.focus();
                    isAuthenticate = false;
                },
                close: function() {
                    if (isAuthenticate) {
                        REMOVE_UNIT_CSV_ID = $(event).attr("data-csv-id");
                        removeClientUnitCsvData(REMOVE_UNIT_CSV_ID, groupId);
                    }
                }
            });
        }
    })
}

function removeClientUnitCsvData(REMOVE_UNIT_CSV_ID, groupId) {
    displayLoader();
    function onSuccess(data) {
        var tblR4 = '', clone4 = '';
        CURRENT_PASWORD.val('');
        $('.details').show();
        rejectedUnitData = data.rejected_unit_data;
        if (rejectedUnitData.length == 0) {
            $('.tbody-compliance').empty();
            tblR4 = $('#nocompliance_templates '+
                '.table-nocompliances-list .table-row');
            clone4 = tblR4.clone();
            $('.tbl-norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            REPORT_VIEW.show();
            hideLoader();
        } else {
            hideLoader();
            REPORT_VIEW.show();
            loadCountwiseResult(rejectedUnitData);
        }
        displaySuccessMessage(message.record_deleted);
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    filterData = {
        "csv_id": parseInt(REMOVE_UNIT_CSV_ID),
        "bu_client_id": parseInt(groupId)
    };

    bu.deleteRejectedUnitByCsvID(filterData, function(error, response) {
        if (error == null) {
            onSuccess(response)
        } else {
            onFailure(error);
        }
    });
    hideLoader();
}

// download rejected client unit data
function downloadClick(csvId, event) {
    var downloadFileFormat = $(event).attr("data-format");
    var grpId = GROUP_ID.val();
    displayLoader();
    function onSuccess(data) {
        var updatedCount = 0;
        var dataCSVid = 0;
        var downloadCount = 0;
        var eventID = "download_files_";

        updatedCount = data.updated_unit_count;
        dataCSVid = updatedCount[0].csv_id;
        downloadCount = updatedCount[0].download_count;
        if (parseInt(downloadCount) == 1) {
            eventID = eventID + dataCSVid;
            document.getElementById(eventID).classList.toggle("show");
            $("#delete_action_" + dataCSVid).attr("style", "display:block");

        } else if (parseInt(downloadCount) >= REJECTED_FILE_DOWNLOADCOUNT) {
            eventID = eventID + dataCSVid;
            document.getElementById(eventID).classList.toggle("show");
            $("#delete_action_" + dataCSVid).attr("style", "display:block");
            $("#download_files_" + dataCSVid).remove();
            $("#download_icon_" + dataCSVid).remove();
        }
        displaySuccessMessage(message.download_files);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    //csv_id
    filterData = {
        "csv_id": parseInt(csvId)
    };

    requestDownloadData = {
        "csv_id": parseInt(csvId),
        "cg_id": parseInt(grpId),
        "download_format": downloadFileFormat
    };

    bu.updateDownloadClickCount(filterData, function(error, response) {
        if (error == null) {
            onSuccess(response);
            requestDownload(requestDownloadData, downloadFileFormat);
        } else {
            onFailure(error);
        }
    });
    hideLoader();
    return false;
}

function requestDownload(requestDownloadData, downloadFileFormat) {
    bu.downloadRejectedClientUnitReport(requestDownloadData,
        function(error, response) {
            if (error == null) {
                if (downloadFileFormat == "csv") {
                    $(location).attr('href', response.csv_link);
                    hideLoader();
                }
                else if (downloadFileFormat == "excel") {
                    $(location).attr('href', response.xlsx_link);
                    hideLoader();
                }
                else if (downloadFileFormat == "text") {
                    $.get(response.txt_link, function(data){
                        url = response.txt_link
                        txt_file_name = url.substring(url.lastIndexOf('/')+1)
                        download(txt_file_name, "text/plain", data);
                    },
                    'text');
                    hideLoader();
                }
                else if (downloadFileFormat == "ods") {
                    $(location).attr('href', response.ods_link);
                    hideLoader();
                }
            }
            else {
                hideLoader();
            }
        });
}

// download text format rejected client unit data
function download(filename, mime_type, text) {
    var element = document.createElement('a');
    var href = 'data:'+mime_type+';charset=utf-8,'+encodeURIComponent(text);
    element.setAttribute('href', href);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

/* DownloadFileOptionList - Excel,CSV,ODS,Text  */
function rejectedFiles(event) {
    var eventID = $(event).attr("data-id");
    eventID = "download_files_" + eventID;
    document.getElementById(eventID).classList.toggle("show");
}

function resetFilter() {
    $('.tbody-usermappingdetails-list').empty();
    REPORT_VIEW.hide();
    $('.details').hide();
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i, openDropdown;
        for (i = 0; i < dropdowns.length; i++) {
            openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// Initial functions load
$(function() {
    bu.getLoadConstants();
    REPORT_VIEW.hide();
    initialize();
    pageControls();
});