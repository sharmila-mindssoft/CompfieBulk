var GROUP_NAME = $('#groupval');
var GROUP_ID = $('#group');
var AC_GROUP = $('#ac-group');
var SHOW_BTN = $('#show');
var REPORT_VIEW = $('.grid-table-rpt');
var PASSWORD_SUBMIT_BUTTON = $('#password-submit');
var CURRENT_PASWORD = $('#current-password');
var REMOVE_UNIT_CSV_ID;
var EXISTING_USER_ID = [];
var ALL_USER_INFO = '';
var USER_CATEGORY_ID = 0;
var CLIENT_LIST;
var rejClientUnit = new RejectedClientUnitBulk();
function RejectedClientUnitBulk() {}

// Handle All Page Controls like Button submit
function pageControls() {
    //load group form list in autocomplete text box
    GROUP_NAME.keyup(function(e) {
        console.log("Groups");
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
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    var currentId = idElement[0].id;
}

// Get Client Unit Rejected report data from api
function processSubmit() {
    var groupId = parseInt(GROUP_ID.val());

    displayLoader();
    filterdata = {
        "bu_client_id": groupId
    };

    function onSuccess(data) {
        $('.details').show();
        rejClientUnitData = data.rejected_unit_data;
        if (rejClientUnitData.length == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates ' +
                '.table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
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

    bu.getClientUnitRejectedData(filterdata, function(error, response) {
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
    var csvId;
    var csvName;
    var totalNoOfTasks;
    var rejectedOn;
    var reasonForRejection;
    var statutoryAction;
    var rejectedBy;
    var declinedCount;
    var fileDownloadCount;
    var isFullyRejected;
    var deleteStatus;
    $('.tbody-compliance').empty();
    for (var entity in data) {
        deleteStatus = '';
        sno = parseInt(sno) + 1;
        csvId = data[entity].csv_id;
        csvName = data[entity].csv_name;
        totalNoOfTasks = data[entity].total_records;
        rejectedOn = data[entity].rejected_on;
        rejectedBy = data[entity].rejected_by;
        isFullyRejected = data[entity].is_fully_rejected;
        statutoryAction = data[entity].statutory_action;
        fileDownloadCount = data[entity].file_download_count;
        rejectedReason = data[entity].rejected_reason;
        declinedCount = data[entity].declined_count;
        rejectedFileName = data[entity].rejected_file;

        if (parseInt(isFullyRejected) == IS_FULLY_REJECT_ACTION_STATUS) {
            removeHrefTag = '';
            reasonForRejection = rejectedReason;
            $(ALL_USER_INFO).each(function(key, value) {
                if (parseInt(rejectedBy) == value["user_id"]) {
                    EmpCode = value["employee_code"];
                    EmpName = value["employee_name"];
                    rejectedBy = EmpCode + " - " + EmpName.toUpperCase();
                }
            });
        } else if (parseInt(statutoryAction) == SYSTEM_REJECT_ACTION_STATUS) {
            rejectedBy = SYSTEM_REJECTED_BY;
            reasonForRejection = '';
        }
        var tblRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tblRow1.clone();

        $('.tbl_sno', clone1).text(sno);
        $('.tbl_upload_filename', clone1).text(csvName);
        $(".tbl_rejected_on", clone1).text(rejectedOn);
        $('.tbl_rejected_by', clone1).text(rejectedBy);
        $('.tbl_no_of_tasks', clone1).text(totalNoOfTasks);
        $('.tbl_declined_count', clone1).text(declinedCount);
        $('.tbl_reason_for_rejection', clone1).text(reasonForRejection);

        $('.tbl_remove .remove_a', clone1).attr({
            'id': "delete_action_" + csvId,
            'data-csv-id': csvId,
            onClick: "confirm_alert(this)",
        });

        /***** Rejected File Downloads ********/
        if (parseInt(fileDownloadCount) < REJECTED_FILE_DOWNLOADCOUNT) {
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
        if (parseInt(fileDownloadCount) < SHOW_REMOVE_ICON){
            $('.tbl_remove .remove_a', clone1).addClass("default-display-none");
        }
        $('#datatable-responsive .tbody-compliance').append(clone1);
    }
    hideLoader();
}

// Fields Manadory validation
RejectedClientUnitBulk.prototype.validateMandatory = function() {
    isValid = true;

    if (GROUP_NAME.val().trim().length == 0) {
        displayMessage(message.group_required);
        isValid = false;
    }
    return isValid;
};

//Initialize the page load user list
function initialize() {
    function onSuccess(data) {
        CLIENT_LIST = data.client_group_list;
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

//validate password
function validateAuthentication() {
    var password = CURRENT_PASWORD.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CURRENT_PASWORD.focus();
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
            CURRENT_PASWORD.val('');
        } else {
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
                target: '#custom-modal-approve',
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
        CURRENT_PASWORD.val('');
        $('.details').show();
        rejectedUnitData = data.rejected_unit_data;
        if (rejectedUnitData.length == 0) {
            $('.tbody-compliance').empty();
            var tblR4 = $('#nocompliance-templates '+
                '.table-nocompliances-list .table-row');
            var clone4 = tblR4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
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

    filterdata = {
        "csv_id": parseInt(REMOVE_UNIT_CSV_ID),
        "bu_client_id": parseInt(groupId)
    };

    bu.deleteRejectedUnitByCsvID(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response)
        } else {

            onFailure(error);
        }
    });
    hideLoader();
}

function downloadClick(csvId, event) {
    var downloadFileFormat = $(event).attr("data-format");
    var grpId = GROUP_ID.val();

    displayLoader();

    function onSuccess(data) {
        var updatedCount;
        var dataCSVid;
        var downloadCount;
        var eventID = "download_files_";

        updatedCount = data.updated_unit_count;

        dataCSVid = updatedCount[0].csv_id;
        downloadCount = updatedCount[0].download_count;
        if (parseInt(downloadCount) == SHOW_REMOVE_ICON) {
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
    filterdata = {
        "csv_id": parseInt(csvId)
    };

    requestDownloadData = {
        "csv_id": parseInt(csvId),
        "cg_id": parseInt(grpId),
        "download_format": downloadFileFormat
    };

    bu.updateDownloadClickCount(filterdata, function(error, response) {
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
                } else if (downloadFileFormat == "excel") {
                    $(location).attr('href', response.xlsx_link);
                    hideLoader();
                } else if (downloadFileFormat == "text") {
                    $(location).attr('href', response.txt_link);
                    hideLoader();
                } else if (downloadFileFormat == "ods") {
                    $(location).attr('href', response.ods_link);
                    hideLoader();
                }
            } else {
                hideLoader();
            }
        });
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
    mirror.getLoadConstants();
    REPORT_VIEW.hide();
    initialize();
    pageControls();
});