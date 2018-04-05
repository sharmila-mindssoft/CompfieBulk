var COUNTRY_LIST;
var CLIENT_LIST;
var LEGAL_ENTITY_LIST;
var ASSIGNED_UNIT_LIST;

var DOMAINS_LIST = [];
var REMOVE_UNIT_CSV_ID;
var CHECK_DUPLICATE_USER_ID = [];
var ALL_USER_INFO = '';
var DOMAIN_LIST = '';
var COUNTRY_WISE_DOMAIN = '';
var USER_CATEGORY_ID = 0;

var GROUP_NAME = $('#cgroupval');
var GROUP_ID = $('#cgroup-id');
var AC_GROUP = $('#ac-cgroup');
var SHOW_BTN = $('#show');
var REPORT_VIEW = $('.grid-table-rpt');
var PASSWORD_SUBMIT_BUTTON = $('#password-submit');
var CURRENT_PASSWORD = $('#current-password');
var AC_LEGAL_ENTITY = $('#ac-legalentity');
var AC_UNIT = $('#ac-unit');
var LEGAL_ENTITY_VAL = $('#legalentityval');
var LEGAL_ENTITY = $('#legalentityid');
var UNIT_VAL = $('#unitval');
var UNIT = $('#unitid');
var DOMAIN = $('#domain');

/**** User Level Category ***********/

ASM_BULK_REPORT_CLASS = new assignStatutoryBulkReport();

function pageControls() {
    //load group form list in autocomplete text box
    GROUP_NAME.keyup(function(e) {
        var textVal = $(this).val();
        commonAutoComplete(
            e, AC_GROUP, GROUP_ID, textVal,
            _clients, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GROUP_NAME, GROUP_ID, val);
            });
        resetFilter('clients');
    });

    //load legalentity form list in autocomplete text box
    LEGAL_ENTITY_VAL.keyup(function(e) {
        resetFilter('le');
        var textVal = $(this).val();
        var legalEntityList = [];
        var clientId = GROUP_ID.val();
        var conditionFields = [];
        var conditionValues = [];
        var i, j;
        var dataClient, dataLE;

        if (GROUP_ID.val() > 0) {

            if (GROUP_ID.val() != '') {
                conditionFields.push("client_id");
                conditionValues.push(GROUP_ID.val());
            }
            dataClient = CLIENT_LIST;
            dataLE = LEGAL_ENTITY_LIST;

            for (i = 0; i < dataClient.length; i++) {
                if ((dataClient[i].client_id == clientId)) {
                    for (j = 0; j < dataLE.length; j++) {
                        if (dataLE[j].legal_entity_id == dataClient[i].legal_entity_id) {
                            legalEntityList.push({
                                "client_id": dataClient[i].client_id,
                                "business_group_id": dataLE[j].business_group_id,
                                "legal_entity_id": dataLE[j].legal_entity_id,
                                "legal_entity_name": dataLE[j].legal_entity_name
                            });
                        }
                    }
                }
            }
            commonAutoComplete(
                e, AC_LEGAL_ENTITY, LEGAL_ENTITY, textVal,
                legalEntityList, "legal_entity_name", "legal_entity_id",
                function(val) {
                    onAutoCompleteSuccess(LEGAL_ENTITY_VAL, LEGAL_ENTITY, val);
                    loadDomains();
                }, conditionFields, conditionValues);

        }
    });

    DOMAIN.on('change', function(e) {
        resetFilter('domains');
    });

    UNIT_VAL.keyup(function(e) {

    isValid = ASM_BULK_REPORT_CLASS.validateMandatory();
    if(isValid == true)
    {
        var clientId = GROUP_ID.val();
        var legalEntityId = LEGAL_ENTITY.val();
        var domainIds = DOMAIN.val();
        var textVal = $(this).val();
        var unitList = [];
        var selectedDomain = [];
        var i, j;
        if (domainIds) {
            $.each(domainIds, function(key, value) {
                selectedDomain.push(parseInt(value));
            });
        }
        if (clientId > 0 && legalEntityId > 0 && domainIds.length > 0) {
            for (i = 0; i < ASSIGNED_UNIT_LIST.length; i++) {

                if (ASSIGNED_UNIT_LIST[i].client_id == clientId &&
                    ASSIGNED_UNIT_LIST[i].legal_entity_id == legalEntityId &&
                    $.inArray(ASSIGNED_UNIT_LIST[i].d_id, selectedDomain) >= 0)
                {

                    unitCodeName = ASSIGNED_UNIT_LIST[i].unit_code_name;
                    unitCode = unitCodeName.split("-");
                    unitCode = unitCode[0];
                    unitList.push({
                        "unit_id": unitCode,
                        "unit_name": unitCodeName
                    });
                }
            }
            commonAutoComplete(
                e, AC_UNIT, UNIT, textVal,
                unitList, "unit_name", "unit_id",
                function(val) {
                    onAutoCompleteSuccess(UNIT_VAL, UNIT, val);
                });
        }
    }
    });

    SHOW_BTN.click(function() {
        isValid = ASM_BULK_REPORT_CLASS.validateMandatory();
        if (isValid == true) {
            $('#mapping_animation').removeClass().addClass('bounceInLeft '+
                'animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd ' +
                    'oanimationend animationend',
                    function() {
                        $(this).removeClass();
                    });
            processSubmit();
        }
    });
}

function getDomainByCountryID(COUNTRY_LIST) {
    var sText = '';
    var str = '';
    $.each(COUNTRY_LIST, function(key, countryId) {
        var cId = countryId;
        var flag = true;
        $.each(DOMAIN_LIST, function(key1, v) {
            if (v.is_active == false) {
                return;
            }
            if ($.inArray(cId, v.country_ids) >= 0) {
                var dVal = v.domain_id;
                str += '<option value="' + dVal + '" ' + sText + '>' +
                    v.domain_name + '</option>';
                flag = false;
            }
        });
    });
    DOMAIN.append(str);
    DOMAIN.multiselect('rebuild');
}


/******** Load Domain Lists *********/
function loadDomains() {
    var clientId = GROUP_ID.val();
    var legal_id = LEGAL_ENTITY.val();
    var APIClientID;
    var APILegalEntityID;
    var COUNTRY_LIST = [];
    $.each(CLIENT_LIST, function(key, value) {
        APIClientID = parseInt(value["client_id"]);
        APILegalEntityID = parseInt(value["legal_entity_id"]);
        if (clientId == APIClientID && legal_id == APILegalEntityID) {
            COUNTRY_LIST.push(parseInt(value["country_id"]));
        }
    });
    getDomainByCountryID(COUNTRY_LIST);
}


function onAutoCompleteSuccess(valueElement, idElement, val) {
    var currentId;
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();

    currentId = idElement[0].id;
    if (currentId == 'cgroup-id') {
        resetFilter('clients');
    } else if (currentId == 'domain') {
        resetFilter('domains');
    } else if (currentId == 'legalentityid') {
        resetFilter('le');
    } else if (currentId == 'unitid') {
        resetFilter('unit');
    }
}


function resetFilter(evt) {
    if (evt == 'clients') {
        LEGAL_ENTITY_VAL.val('');
        LEGAL_ENTITY.val('');
        DOMAIN.empty();
        DOMAIN.html();
        DOMAIN.multiselect('rebuild');
        UNIT_VAL.val('');
        UNIT.val('');
    }
    if (evt == 'le') {
        DOMAIN.empty();
        DOMAIN.html();
        DOMAIN.multiselect('rebuild');

        UNIT_VAL.val('');
        UNIT.val('');

    }
    if (evt == 'domains') {
        UNIT_VAL.val('');
        UNIT.val('');
    }
    $('.tbody-usermappingdetails-list').empty();
    REPORT_VIEW.hide();
    $('.details').hide();
}


function resetFields() {
    GROUP_ID.val('');
    LEGAL_ENTITY.val('');
    UNIT.val('');
}


function fetchFiltersData() {
    displayLoader();
    mirror.getClientLoginTraceFilter(
        function(error, response) {

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
    var currentId;
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    currentId = idElement[0].id;
}
// get statutory mapping report data from api
function processSubmit() {

    var clientId = parseInt(GROUP_ID.val());
    var legalEntityId = parseInt(LEGAL_ENTITY.val());
    var domainIds = DOMAIN.val();
    var unitId = '';
    var selectedDomain = [];

    if (UNIT.val()) {
        unitId = UNIT.val();
    }
    $.each(domainIds, function(key, value) {
        selectedDomain.push(parseInt(value));
    });
    displayLoader();
    requestData = {
        "client_id": clientId,
        "le_id": legalEntityId,
        "domain_ids": selectedDomain,
        "asm_unit_code": unitId
    };

    function onSuccess(data) {
        var tr, trRow;
        $('.details').show();
        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd '+
                'oanimationend' +
                ' animationend',
                function() {
                    $(this).removeClass();
                    $(this).show();
                });

        rejectedAssignSMData = data.asm_rejected_data;

        if (rejectedAssignSMData.length == 0) {
            $('.tbody-compliance').empty();

            tr = $('#nocompliance-templates .table-nocompliances-list' +
                ' .table-row');
            trRow = tr.clone();

            $('.tbl_norecords', trRow).text('No Records Found');
            $('.tbody-compliance').append(trRow);
            REPORT_VIEW.show();
            hideLoader();
        } else {
            hideLoader();
            REPORT_VIEW.show();
            loadCountwiseResult(rejectedAssignSMData);
        }
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    bu.getRejectedAssignSMData(requestData, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

//display statutory mapping details accoring to count
function loadCountwiseResult(filterList) {
    sNo = 0;
    var csvId;
    var CSVName;
    var totalNoOfTasks;
    var rejectedOn;
    var reasonRejection;
    var statutoryAction;
    var rejectedBy;
    var declinedCount;
    var fileDownloadCount;
    var reasonRejectionComment;
    var entity;
    var tr, trRow;
    $('.tbody-compliance').empty();
    for (entity in filterList) {
        sNo = parseInt(sNo) + 1;
        csvId = filterList[entity].csv_id;
        CSVName = filterList[entity].csv_name;
        totalNoOfTasks = filterList[entity].total_records;
        rejectedOn = filterList[entity].rejected_on;
        isFullyRejected = filterList[entity].is_fully_rejected;
        statutoryAction = filterList[entity].statutory_action;
        fileDownloadCount = filterList[entity].file_download_count;
        reasonRejection = filterList[entity].rejected_reason;

        if (parseInt(isFullyRejected) == IS_FULLY_REJECT_ACTION_STATUS) {

            reasonRejectionComment = reasonRejection;
            $(ALL_USER_INFO).each(function(key, value) {
                if (parseInt(filterList[entity].rejected_by) == value["user_id"]) {
                    empCode = value["employee_code"];
                    empName = value["employee_name"];
                    rejectedBy = empCode + " - " + empName;
                }
            });
        } else if (parseInt(statutoryAction) == SYSTEM_REJECT_ACTION_STATUS) {

            rejectedBy = SYSTEM_REJECTED_BY;
            declinedCount = filterList[entity].declined_count;
            reasonRejectionComment = '';
        }

        tr = $('#act-templates .table-act-list .table-row-act-list');
        trRow = tr.clone();

        $('.tbl_sno', trRow).text(sNo);
        $('.tbl_upload_filename', trRow).text(CSVName);
        $(".tbl_rejected_on", trRow).text(rejectedOn);
        $('.tbl_rejected_by', trRow).text(rejectedBy);
        $('.tbl_no_of_tasks', trRow).text(totalNoOfTasks);
        $('.tbl_declined_count', trRow).text(declinedCount);
        $('.tbl_reason_for_rejection', trRow).text(reasonRejectionComment);

        $('.tbl_remove .remove_a', trRow).attr({
            'id': "delete_action_" + csvId,
            'data-csv-id': csvId,
            onClick: "confirm_alert(this)",
        });

        /***** Rejected File Downloads ********/
        if (parseInt(fileDownloadCount) < REJECTED_FILE_DOWNLOADCOUNT) {
            $('.tbl_rejected_file .rejected_i_cls', trRow).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)"
            });
            $('.tbl_rejected_file .rejected_div_cls', trRow).attr({
                'id': "download_files_" + csvId
            });
            $('.tbl_rejected_file .rejected_div_cls .rej_excel, .rej_csv, ' +
                '.rej_ods, .rej_text', trRow).attr({
                onclick: "downloadClick(" + csvId + ",this)"
            });
        } else {
            $('.tbl_rejected_file .rejected_i_cls', trRow).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)",
            });
            $('.tbl_rejected_file .rejected_i_cls', trRow)
                .addClass("default-display-none");
        }
        if (parseInt(fileDownloadCount) < SHOW_REMOVE_ICON) {
            $('.tbl_remove .remove_a', trRow).addClass("default-display-none");
        }

        $('#datatable-responsive .tbody-compliance').append(trRow);
    }
    hideLoader();
}


function assignStatutoryBulkReport() {}
// Fields Manadory validation
assignStatutoryBulkReport.prototype.validateMandatory = function() {
    isValid = true;
    if (GROUP_NAME.val().trim().length == 0) {
        displayMessage(message.client_group_required);
        isValid = false;
    } else if (LEGAL_ENTITY.val().trim().length == 0) {
        displayMessage(message.legalentity_required);
        isValid = false;
    } else if ($('#domain option:selected').text() == "") {
        displayMessage(message.domain_required);
        isValid = false;
    }
    return isValid;
};


//load all the filters
function initialize() {
    function onSuccess(data) {
        ALL_USER_INFO = data.user_details;
        userDetails = data.user_details[0];
        DOMAIN_LIST = data.domains;
        COUNTRY_WISE_DOMAIN = data.country_wise_domain;
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

//load all the filters
function UserGroupDetails() {
    function onSuccess(data) {
        CLIENT_LIST = data.usermapping_groupdetails;
        LEGAL_ENTITY_LIST = data.usermapping_legal_entities;
        ASSIGNED_UNIT_LIST = data.statutory_unit;
        resetAllfilter();
        resetFields();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();

    mirror.getUserMappingStatutoryFilters(function(error, response) {
        if (error == null) {
            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}

function loadCurrentUserDetails() {
    var user = mirror.getUserInfo();
    var loggedUserId = 0;
    if (ALL_USER_INFO) {
        $.each(ALL_USER_INFO, function(key, value) {
            if (user.user_id == value["user_id"]) {
                USER_CATEGORY_ID = value["user_category_id"];
                loggedUserId = value["user_id"];
            }
        });
    }
    if (USER_CATEGORY_ID == TE_USER_CATEGORY) {
        // TE-Name  : Techno-Executive
        $('.active-techno-executive').attr('style', 'display:block');
        $('#techno-name').text(user.employee_code + " - " +
            user.employee_name);
        CHECK_DUPLICATE_USER_ID.push(loggedUserId);
    } else if (USER_CATEGORY_ID == TM_USER_CATEGORY &&
        USER_CATEGORY_ID != TE_USER_CATEGORY &&
        loggedUserId > 0) {
        // TE-Name  : Techno-Manager
        getUserMappingsList(loggedUserId);
    }
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
            CURRENT_PASSWORD.empty();
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
    CURRENT_PASSWORD.val("");

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
                    CURRENT_PASSWORD.focus();
                    isAuthenticate = false;
                },
                close: function() {
                    if (isAuthenticate) {
                        REMOVE_UNIT_CSV_ID = $(event).attr("data-csv-id");
                        RemoveStatutoryCsvData(REMOVE_UNIT_CSV_ID, groupId);
                    }
                }
            });
        }
    })
}


function RemoveStatutoryCsvData(REMOVE_UNIT_CSV_ID, groupId) {
    var clientId = parseInt(GROUP_ID.val());
    var legalEntityId = parseInt(LEGAL_ENTITY.val());
    var domainIds = DOMAIN.val();
    var unitId = UNIT.val();
    var selectedDomain = [];

    $.each(domainIds, function(key, value) {
        selectedDomain.push(parseInt(value));
    });
    requestData = {
        "client_id": clientId,
        "le_id": legalEntityId,
        "domain_ids": selectedDomain,
        "asm_unit_code": unitId,
        "csv_id": parseInt(REMOVE_UNIT_CSV_ID)
    };
    displayLoader();

    function onSuccess(data) {
        $('.details').show();
        $('.details').show();
        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd '+
                'oanimationend' +
                ' animationend',
                function() {
                    $(this).removeClass();
                    $(this).show();
                });
        rejectedASMData = data.asm_rejected_data;
        if (rejectedASMData.length == 0) {
            $('.tbody-compliance').empty();
            var tr = $('#nocompliance-templates .table-nocompliances-list ' +
                '.table-row');
            var trRow = tr.clone();
            $('.tbl_norecords', trRow).text('No Records Found');
            $('.tbody-compliance').append(trRow);
            REPORT_VIEW.show();
            hideLoader();
        } else {
            hideLoader();
            REPORT_VIEW.show();
            loadCountwiseResult(rejectedASMData);
        }
        displaySuccessMessage(message.record_deleted);
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    bu.deleteRejectedASMByCsvID(requestData, function(error, response) {
        if (error == null) {
            onSuccess(response)
        } else {
            onFailure(error);
        }
    });
    hideLoader();
}

function downloadClick(csv_id, event) {
    var downloadFileFormat = $(event).attr("data-format");
    var clientId = parseInt(GROUP_ID.val());
    var legalEntityId = parseInt(LEGAL_ENTITY.val());
    var domainIds = DOMAIN.val();
    var unitId = '';
    var selectedDomain = [];
    if (UNIT.val()) {
        unitId = UNIT.val();
    }
    $.each(domainIds, function(key, value) {
        selectedDomain.push(parseInt(value));
    });
    displayLoader();

    function onSuccess(data) {
        var updatedCount;
        var dataCSVid;
        var downloadCount;
        var eventID = "download_files_";

        updatedCount = data.asm_updated_count;

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
    requestData = {
        "csv_id": parseInt(csv_id)
    };

    requestDownloadData = {
        "client_id": clientId,
        "le_id": legalEntityId,
        "domain_ids": selectedDomain,
        "asm_unit_code": unitId,
        "csv_id": csv_id,
        "download_format": downloadFileFormat
    };

    bu.updateASMDownloadClickCount(requestData, function(error, response) {
        if (error == null) {
            onSuccess(response)

            requestDownload(requestDownloadData, downloadFileFormat);

        } else {
            onFailure(error);
        }
    });
    return false;
}

function requestDownload(requestDownloadData, downloadFileFormat) {
    bu.downloadRejectedASMReportData(requestDownloadData,
        function(downladError, downladResponse) {
            if (downladError == null) {
                if (downloadFileFormat == "csv") {
                    $(location).attr('href', downladResponse.csv_link);
                    hideLoader();
                } else if (downloadFileFormat == "excel") {
                    $(location).attr('href', downladResponse.xlsx_link);
                    hideLoader();
                } else if (downloadFileFormat == "text") {
                    $(location).attr('href', downladResponse.txt_link);
                    hideLoader();
                } else if (downloadFileFormat == "ods") {
                    $(location).attr('href', downladResponse.ods_link);
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


function resetAllfilter() {
    GROUP_NAME.val('');
    LEGAL_ENTITY_VAL.val('');
    UNIT_VAL.val('');
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
    UserGroupDetails();
    fetchFiltersData();
    pageControls();
});