var FULLYREJECTED = "Fully Rejected";
var SYSTEMREJECTED = "COMPFIE";

var GROUPNAME = $('#countryval');
var GROUPID = $('#country');
var ACGROUP = $('#ac-country');


var SHOWBTN = $('#show');
var REPORTVIEW = $('.grid-table-rpt');
var PASSWORDSUBMITBUTTON = $('#password-submit');
var CURRENTPASSWORD = $('#current-password');
var REMOVEUNITCSVID;
var EXISTINGUSERID = [];
var ALLUSERINFO = '';
var USERCATEGORYID = 0;

var rejClientUnit = new RejectedClientUnitBulk();

function RejectedClientUnitBulk() {}

// Handle All Page Controls like Button submit
function pageControls() {
    //load group form list in autocomplete text box
    GROUPNAME.keyup(function(e) {
        console.log("Groups");
        var textVal = $(this).val();
        commonAutoComplete(
            e, ACGROUP, GROUPID, textVal,
            _clients, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GROUPNAME, GROUPID, val);
            });

        resetFilter();
    });

    SHOWBTN.click(function() {
        isValid = rejClientUnit.validateMandatory();
        if (isValid == true) {
            $('#mapping_animation')
                .removeClass()
                .addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd ' +
                    'oanimationend animationend',
                    function() {
                        $(this).removeClass();
                    });
            processSubmit();
        }
    });
}

// 
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

function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    var currentId = idElement[0].id;
}

// Get Client Unit Rejected report data from api
function processSubmit() {
    var groupId = parseInt(GROUPID.val());

    displayLoader();
    filterdata = {
        "bu_client_id": groupId
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
        rejClientUnitData = data.rejected_unit_data;
        if (rejClientUnitData.length == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates ' +
                '.table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            REPORTVIEW.show();
            hideLoader();
        } else {
            hideLoader();
            REPORTVIEW.show();
            loadCountwiseResult(rejClientUnitData);
        }
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    bu.getClientUnitRejectedData(filterdata, function(error, response) {
        console.log("error");
        console.log(error);
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

// Display Rejected Client Unit details accoring to count
function loadCountwiseResult(filterList) {
    var sno = 0;
    var csvId;
    var csvName;
    var totalNoOfTasks;
    var rejectedOn;
    var reasonForRejection;
    var statutoryAction;
    var removeHrefTag;
    var rejectedBy;
    var declinedCount;
    var fileDownloadCount;
    var isFullyRejected;
    var deleteStatus;
    $('.tbody-compliance').empty();
    for (var entity in filterList) {
        deleteStatus = '';
        sno = parseInt(sno) + 1;
        csvId = filterList[entity].csv_id;
        csvName = filterList[entity].csv_name;
        totalNoOfTasks = filterList[entity].total_records;
        rejectedOn = filterList[entity].rejected_on;
        isFullyRejected = filterList[entity].is_fully_rejected;
        statutoryAction = filterList[entity].statutory_action;
        fileDownloadCount = filterList[entity].file_download_count;
        rejectedBy = filterList[entity].rejected_by;
        if (parseInt(isFullyRejected) == 1) {
            removeHrefTag = '';
            reasonForRejection = FULLYREJECTED;
            $(ALLUSERINFO).each(function(key, value) {
                if (parseInt(rejectedBy) == value["user_id"]) {
                    EmpCode = value["employee_code"];
                    EmpName = value["employee_name"];
                    rejectedBy = EmpCode + " - " + EmpName.toUpperCase();
                }
            });
        } else if (parseInt(statutoryAction) == 3) {
            rejectedBy = SYSTEMREJECTED;
            declinedCount = filterList[entity].declined_count;
            reasonForRejection = '';
        }

        if (parseInt(fileDownloadCount) < 1) {
            deleteStatus = 'style="display:none;"';
        }
        console.log(parseInt(fileDownloadCount));
        console.log(parseInt(fileDownloadCount) < 1);
        console.log(deleteStatus);

        var tblRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tblRow1.clone();

        $('.tbl_sno', clone1).text(sno);
        $('.tbl_upload_filename', clone1).text(csvName);
        $(".tbl_rejected_on", clone1).text(rejectedOn);
        $('.tbl_rejected_by', clone1).text(rejectedBy);
        $('.tbl_no_of_tasks', clone1).text(totalNoOfTasks);
        $('.tbl_declined_count', clone1).text(declinedCount);
        $('.tbl_reason_for_rejection', clone1).text(reasonForRejection);

        /***** Rejected File Downloads ********/
        if (parseInt(fileDownloadCount) < 2) {
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
        $('.tbl_remove .remove_a', clone1).attr({
            'id': "delete_action_" + csvId,
            'data-csv-id': csvId,
            onClick: "confirm_alert(this)"
        });
        $('#datatable-responsive .tbody-compliance').append(clone1);
    }
    hideLoader();
}

// Fields Manadory validation
RejectedClientUnitBulk.prototype.validateMandatory = function() {
    isValid = true;

    if (GROUPNAME.val().trim().length == 0) {
        displayMessage(message.group_required);
        isValid = false;
    }
    return isValid;
};

//Initialize the page load user list
function initialize() {
    function onSuccess(data) {
        ALLUSERINFO = data.user_details;
        userDetails = data.user_details[0];
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

function loadCurrentUserDetails() {
    //alert('load Current User Details');
    var user = mirror.getUserInfo();
    var loggedUserId = 0;
    if (ALLUSERINFO) {
        $.each(ALLUSERINFO, function(key, value) {
            if (user.user_id == value["user_id"]) {
                USERCATEGORYID = value["user_category_id"];
                loggedUserId = value["user_id"];
            }
        });
    }

    if (USERCATEGORYID == 6) {
        // TE-Name  : Techno-Executive
        $('.active-techno-executive').attr('style', 'display:block');
        $('#techno-name').text(user.employee_code + " - " +
            user.employee_name.toUpperCase());
        EXISTINGUSERID.push(loggedUserId);
    } else if (USERCATEGORYID == 5 && USERCATEGORYID != 6 
                                   && loggedUserId > 0) {
        // TE-Name  : Techno-Manager
        getUserMappingsList(loggedUserId);
    }
}

//validate password
function validateAuthentication() {
    var password = CURRENTPASSWORD.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CURRENTPASSWORD.focus();
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
            displaySuccessMessage(message.password_authentication_success);
            CURRENTPASSWORD.empty();
        } else {
            hideLoader();
            if (error == 'InvalidPassword') {
                displayMessage(message.invalid_password);
            }
        }
    });
}

PASSWORDSUBMITBUTTON.click(function() {
    validateAuthentication();
});

function confirm_alert(event) {
    var groupId = GROUPID.val();

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
                    CURRENTPASSWORD.focus();
                    isAuthenticate = false;
                },
                close: function() {
                    if (isAuthenticate) {
                        REMOVEUNITCSVID = $(event).attr("data-csv-id");
                        removeClientUnitCsvData(REMOVEUNITCSVID, groupId);
                    }
                }
            });
        }
    })
}

function removeClientUnitCsvData(REMOVEUNITCSVID, groupId) {
    displayLoader();

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

        rejectedUnitData = data.rejected_unit_data;
        if (rejectedUnitData.length == 0) {
            $('.tbody-compliance').empty();
            var tblR4 = $('#nocompliance-templates '+
                '.table-nocompliances-list .table-row');
            var clone4 = tblR4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            REPORTVIEW.show();
            hideLoader();
        } else {
            hideLoader();
            REPORTVIEW.show();
            loadCountwiseResult(rejectedUnitData);
        }
        displaySuccessMessage(message.record_deleted);

    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    filterdata = {
        "csv_id": parseInt(REMOVEUNITCSVID),
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
    var grpId = GROUPID.val();

    displayLoader();

    function onSuccess(data) {
        var updatedCount;
        var dataCSVid;
        var downloadCount;
        var eventID = "download_files_";

        updatedCount = data.updated_unit_count;

        dataCSVid = updatedCount[0].csv_id;
        downloadCount = updatedCount[0].download_count;
        if (parseInt(downloadCount) == 1) {
            eventID = eventID + dataCSVid;
            document.getElementById(eventID).classList.toggle("show");
            $("#delete_action_" + dataCSVid).attr("style", "display:block");

        } else if (parseInt(downloadCount) >= 2) {
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
    REPORTVIEW.hide();
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
    REPORTVIEW.hide();
    initialize();
    fetchFiltersData();
    pageControls();
    /*tempDatasetup();*/
});

/*function tempDatasetup() {
  $('#countryval').val("India");
  $('#domainval').val("Industrial Law");
  $('#country').val(1);
  $('#domain').val(3);
  SHOWBTN.click();
}
*/