var COUNTRY_LIST;
var CLIENT_LIST;
var LEGAL_ENTITY_LIST;
var ASSIGNED_UNIT_LIST;

var DOMAINS;
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
        resetFilter('clients');
        var textVal = $(this).val();
        commonAutoComplete(
            e, AC_GROUP, GROUP_ID, textVal,
            CLIENT_LIST, "cl_name", "cl_id",
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
                if ((dataClient[i].cl_id == clientId)) {                    
                    for (j = 0; j < dataLE.length; j++) {
                          if (dataLE[j].cl_id == dataClient[i].cl_id) {
                            legalEntityList.push({
                                "client_id": dataClient[i].cl_id,
                                "legal_entity_id": dataLE[j].le_id,
                                "legal_entity_name": dataLE[j].le_name
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
                    fetchDomainMultiselect();
                }, conditionFields, conditionValues);
        }
        resetFilter('le');
    });

    /*DOMAIN.multiselect('selectAll');*/

    DOMAIN.on('change', function(e) {
        /*DOMAIN.selectpicker('refresh');*/
        /*resetFilter('domains');
        if($("#select-deselect").attr("value") == "select-all"
            && this.value == "select-all")
        {
            $("#select-deselect").attr("value", "deselect-all");
            DOMAIN.multiselect('selectAll');
            DOMAIN.multiselect('rebuild');
        }
        else if($("#select-deselect").attr("value") == "deselect-all")
        {
                $(DOMAIN).each(function()
                {
                    $("#select-deselect").attr("value", "select-all");
                    DOMAIN.multiselect('deselectAll');
                    DOMAIN.val('');
                    DOMAIN.multiselect('rebuild');
                });
        }*/
        resetFilter('domains');
    });


    UNIT_VAL.keyup(function(e) {
        resetFilter('units');
        var str = '';
        var unitList = [];
        var textVal = $(this).val();
        if(DOMAIN.val() != null){
            checkDomain = DOMAIN.val().map(Number);
            checkDomain = integerArrayValue(checkDomain);

            if (UNITS.length > 0 && checkDomain.length > 0) {
                for (var i in UNITS) {
                    if(UNITS[i].le_id == LEGAL_ENTITY.val() &&
                        containsAll(checkDomain, UNITS[i].d_ids)
                        ){
                            var ISVALID = true;
                            for(var j in ASSIGNED_UNIT_LIST){
                                if(
                                    ASSIGNED_UNIT_LIST[j].u_id == UNITS[i].u_id &&
                                    $.inArray(
                                        ASSIGNED_UNIT_LIST[j].d_id, UNITS[i].d_ids
                                    ) == 0
                                ){
                                    ISVALID = false;
                                }
                            }
                            if(ISVALID){
                                unitCodeName = UNITS[i].u_name;
                                unitCode = unitCodeName.split("-");
                                unitCode = unitCode[0];
                                unitList.push({
                                    "unit_id": unitCode,
                                    "unit_name": unitCodeName
                                });
                            }   
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


/*function integerArrayValue(arr) {
  return arr.filter(Boolean);
}*/

//load domains into multi select box
function fetchDomainMultiselect() {
    /*var str = '<option id="select-deselect" value="select-all">Select all'+
               '</option>';*/
    var str = '<option value="">Select</option>';
    if (LEGAL_ENTITY_LIST.length > 0) {
        for (var i in LEGAL_ENTITY_LIST) {
            if(LEGAL_ENTITY_LIST[i].le_id == LEGAL_ENTITY.val()){
                DOMAINS = LEGAL_ENTITY_LIST[i].bu_domains;
                for (var j in DOMAINS) {
                    str += '<option value="'+ DOMAINS[j].d_id +'">'+ 
                    DOMAINS[j].d_name +'</option>';
                }
            }                
        }
        DOMAIN.append(str);
        /*DOMAIN.multiselect('rebuild');*/
    }
}

//get information from api for filters 
function fetchData(){
    displayLoader();    
    bu.getClientInfo(function(error, data) {
        if (error == null) {
            /*GROUPNAME.focus();*/
            CLIENT_LIST = data.bu_clients;
            LEGAL_ENTITY_LIST = data.bu_legalentites;
            ASSIGNED_UNIT_LIST = data.bu_assigned_units;
            UNITS = data.bu_units;            
            hideLoader();
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
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
        /*DOMAIN.multiselect('rebuild');*/
        UNIT_VAL.val('');
        UNIT.val('');
    }
    if (evt == 'le') {
        DOMAIN.empty();
        DOMAIN.html();
        /*DOMAIN.multiselect('rebuild');*/

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
    var domainId = DOMAIN.val();
    var unitId = '';
    var selectedDomain = [];

    if (UNIT.val()) {
        unitId = UNIT.val();
    }
    displayLoader();
    requestData = {
        "client_id": clientId,
        "le_id": legalEntityId,
        "d_id": parseInt(domainId),
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
    var rejectedOn, approvedOn;
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
        approvedOn = filterList[entity].approved_on;
        isFullyRejected = filterList[entity].is_fully_rejected;
        statutoryAction = filterList[entity].statutory_action;
        fileDownloadCount = filterList[entity].file_download_count;
        reasonRejection = filterList[entity].rejected_reason;
        declinedCount = '';
        reasonForRejection = '';

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
            rejectedOn = approvedOn;

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
    var domainId = DOMAIN.val();
    var unitId = UNIT.val();

    requestData = {
        "client_id": clientId,
        "le_id": legalEntityId,
        "d_id": parseInt(domainId),
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
    var domainId = DOMAIN.val();
    var unitId = '';
    var selectedDomain = [];
    if (UNIT.val()) {
        unitId = UNIT.val();
    }
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
        "d_id": parseInt(domainId),
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
                    $.get(downladResponse.txt_link, function(data){
                        txt_file_name = downladResponse.txt_link
                        txt_file_name = txt_file_name.split('\\');
                        download(txt_file_name[1], "text/plain", data);
                    },
                    'text');
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
    fetchData();
    pageControls();
});