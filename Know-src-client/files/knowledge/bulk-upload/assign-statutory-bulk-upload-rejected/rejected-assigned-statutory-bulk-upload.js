var GROUP_NAME = $('#cgroupval');
var GROUP_ID = $('#cgroup_id');
var AC_GROUP = $('#ac_cgroup');
var SHOW_BTN = $('#show');
var REPORT_VIEW = $('.grid-table-rpt');
var PASSWORD_SUBMIT_BUTTON = $('#password_submit');
var CURRENT_PASSWORD = $('#current_password');
var AC_LEGAL_ENTITY = $('#ac_legalentity');
var AC_UNIT = $('#ac_unit');
var LEGAL_ENTITY_VAL = $('#legalentityval');
var LEGAL_ENTITY = $('#legalentityid');
var UNIT_VAL = $('#unitval');
var UNIT = $('#unitid');
var DOMAIN = $('#domainid');
var AC_DOMAIN = $('#ac_domain');
var DOMAIN_VAL = $('#domainval');
var DETAILS = $('.details');
var MAPPING_ANIMATION = $('#mapping_animation');
var TBODY_USERMAPPING_DETAILS = $('.tbody-usermappingdetails-list');
var CLIENT_LIST = '';
var LEGAL_ENTITY_LIST = '';
var ASSIGNED_UNIT_LIST = '';
var DOMAINS = '';
var REMOVE_UNIT_CSV_ID = '';
var ALL_USER_INFO = '';

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
        var i = 0, j = 0;
        var dataClient = '', dataLE = '';
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
                }, conditionFields, conditionValues);
        }
        resetFilter('le');
    });

    //load domain form list in autocomplete text box
    DOMAIN_VAL.keyup(function(e) {
		var i = 0, j = 0;
		var checkDuplicate = [];
		var DOMAIN_LIST = [];
		var textVal = $(this).val();

		resetFilter('domains');
		if (LEGAL_ENTITY_LIST.length > 0) {
			for (i in LEGAL_ENTITY_LIST) {
			    if(LEGAL_ENTITY_LIST[i].le_id == LEGAL_ENTITY.val()){
			        DOMAINS = LEGAL_ENTITY_LIST[i].bu_domains;
			        for (j in DOMAINS) {
			        		DOMAIN_LIST.push({
			                    "domain_id": DOMAINS[j].d_id,
			                    "domain_name": DOMAINS[j].d_name
			                });
			            	checkDuplicate.push(DOMAINS[j].d_id);
			        	}
			    }
			}
			commonAutoComplete(
				e, AC_DOMAIN, DOMAIN, textVal,
				DOMAIN_LIST, "domain_name", "domain_id",
				function(val) {
					onAutoCompleteSuccess(DOMAIN_VAL, DOMAIN, val);
				});
		}
	});

    //load legalentity form list in autocomplete text box
    UNIT_VAL.keyup(function(e) {
        resetFilter('units');
            var str = '';
            var unitList = [];
            var textVal = $(this).val();
            var i = 0, j = 0, ISVALID = '';
            var assignedUid = '', unitsUid = '', aDomainId = '';

            if(DOMAIN.val() != null){
                checkDomain = DOMAIN.val();
                if (UNITS.length > 0 && checkDomain.length > 0) {
                    for (i in UNITS) {
                        if(UNITS[i].le_id == LEGAL_ENTITY.val() &&
                             $.inArray(checkDomain, UNITS[i].d_ids) == -1){
                                ISVALID = true;

                                for(j in ASSIGNED_UNIT_LIST){
                                    assigned_Uid = ASSIGNED_UNIT_LIST[j].u_id;
                                    unitsUid = UNITS[i].u_id;
                                    aDomainId = ASSIGNED_UNIT_LIST[j].d_id;
                                    aUnitId = UNITS[i].d_ids;

                                    if(assigned_Uid == unitsUid &&
                                        $.inArray(aDomainId, aUnitId) == -1) {
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
            MAPPING_ANIMATION.removeClass().addClass('bounceInLeft '+
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

//get information from api for filters 
function fetchData(){
    displayLoader();    
    bu.getClientInfo(function(error, data) {
        if (error == null) {
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
    var currentId = 0;
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();

    currentId = idElement[0].id;
    if (currentId == 'cgroup_id') {
        resetFilter('clients');
    } else if (currentId == 'domainid') {
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
        
		DOMAIN_VAL.val('');
		DOMAIN.val('');

        UNIT_VAL.val('');
        UNIT.val('');
    }
    if (evt == 'le') {
		DOMAIN_VAL.val('');
		DOMAIN.val('');

        UNIT_VAL.val('');
        UNIT.val('');
    }
    if (evt == 'domains') {
        UNIT_VAL.val('');
        UNIT.val('');
    }
    TBODY_USERMAPPING_DETAILS.empty();
    REPORT_VIEW.hide();
    DETAILS.hide();
}


function resetFields() {
    GROUP_ID.val('');
    LEGAL_ENTITY.val('');
    DOMAIN.val('');
    UNIT.val('');
}


function onAutoCompleteSuccess(valueElement, idElement, val) {
    var currentId = 0;
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    currentId = idElement[0].id;
}
// get statutory mapping report data from api
function processSubmit() {
    var clientId = parseInt(GROUP_ID.val());
    var legalEntityId = parseInt(LEGAL_ENTITY.val());
    var domainId =  DOMAIN.val() ? DOMAIN.val() : 0;
    var unitId = UNIT.val() ? UNIT.val() : '';
    var selectedDomain = [];

    displayLoader();
    requestData = {
        "client_id": clientId,
        "le_id": legalEntityId,
        "d_id": parseInt(domainId),
        "asm_unit_code": unitId
    };

    function onSuccess(data) {
        var tr, trRow;
        DETAILS.show();
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

            tr = $('#nocompliance_templates .table-nocompliances-list' +
                ' .table-row');
            trRow = tr.clone();

            $('.tbl-norecords', trRow).text('No Records Found');
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
    var csvId = 0;
    var CSVName = '';
    var totalNoOfTasks = '';
    var rejectedOn = '', approvedOn = '';
    var reasonRejection = '';
    var statutoryAction = '';
    var rejectedBy = '';
    var declinedCount = '';
    var fileDownloadCount = '';
    var reasonRejectionComment = '';
    var entity = '';
    var tr = '', trRow = '', r_by = '';
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

        if (parseInt(isFullyRejected) == 1) {
            reasonRejectionComment = reasonRejection;
            $(ALL_USER_INFO).each(function(key, value) {
                r_by = filterList[entity].rejected_by;
                if (parseInt(r_by) == value["user_id"]) {
                    empCode = value["employee_code"];
                    empName = value["employee_name"];
                    rejectedBy = empCode + " - " + empName;
                }
            });
        } else if (parseInt(statutoryAction) == 3) {

            rejectedBy = SYSTEM_REJECTED_BY;
            rejectedOn = approvedOn;
            declinedCount = filterList[entity].declined_count;
            reasonRejectionComment = '';
        }

        tr = $('#act_templates .table-act-list .table-row-act-list');
        trRow = tr.clone();

        $('.tbl-sno', trRow).text(sNo);
        $('.tbl-upload-filename', trRow).text(CSVName);
        $(".tbl-rejected_on", trRow).text(rejectedOn);
        $('.tbl-rejected-by', trRow).text(rejectedBy);
        $('.tbl-no-of-tasks', trRow).text(totalNoOfTasks);
        $('.tbl-declined-count', trRow).text(declinedCount);
        $('.tbl-reason-for-rejection', trRow).text(reasonRejectionComment);

        $('.tbl-remove .remove-a', trRow).attr({
            'id': "delete_action_" + csvId,
            'data-csv-id': csvId,
            onClick: "confirm_alert(this)",
        });

        /***** Rejected File Downloads ********/
        if (parseInt(fileDownloadCount) < REJECTED_FILE_DOWNLOADCOUNT) {
            $('.tbl-rejected-file .rejected-i-cls', trRow).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)"
            });
            $('.tbl-rejected-file .rejected-div-cls', trRow).attr({
                'id': "download_files_" + csvId
            });
            $('.tbl-rejected-file .rejected-div-cls .rej-excel, .rej-csv, ' +
                '.rej-ods, .rej-text', trRow).attr({
                onclick: "downloadClick(" + csvId + ",this)"
            });
        } else {
            $('.tbl-rejected-file .rejected-i-cls', trRow).attr({
                'id': "download_icon_" + csvId,
                'data-id': csvId,
                onClick: "rejectedFiles(this)",
            });
            $('.tbl-rejected-file .rejected-i-cls', trRow)
                .addClass("default-display-none");
        }
        if (parseInt(fileDownloadCount) < 1) {
            $('.tbl-remove .remove-a', trRow).addClass("default-display-none");
        }
        $('#datatable_responsive .tbody-compliance').append(trRow);
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
                target: '#custom_modal_approve',
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
    var domainId =  DOMAIN.val() ? DOMAIN.val() : 0;
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
        var tr, trRow;
        DETAILS.show();
        DETAILS.show();
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
            tr = $('#nocompliance_templates .table-nocompliances-list ' +
                '.table-row');
            trRow = tr.clone();
            $('.tbl-norecords', trRow).text('No Records Found');
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
    var domainId =  DOMAIN.val() ? DOMAIN.val() : 0;
    var unitId = '';
    var selectedDomain = [];
    if (UNIT.val()) {
        unitId = UNIT.val();
    }
    displayLoader();

    function onSuccess(data) {
        var updatedCount = 0;
        var dataCSVid = 0;
        var downloadCount = 0;
        var eventID = "download_files_";
        updatedCount = data.asm_updated_count;
        dataCSVid = updatedCount[0].csv_id;
        downloadCount = updatedCount[0].download_count;

        if (parseInt(downloadCount) == 1) {
            eventID = eventID + dataCSVid;
            document.getElementById(eventID).classList.toggle("show");
            $("#delete_action_" + dataCSVid).attr("style", "display:block");
        }
        else if (parseInt(downloadCount) >= REJECTED_FILE_DOWNLOADCOUNT) {
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
                        url = downladResponse.txt_link
                        txt_file_name = url.substring(url.lastIndexOf('/')+1)
                        download(txt_file_name, "text/plain", data);
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

/* Download TXT document using Javascript */
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

/* DownloadFileOptionList - Excel,CSV,ODS,Text */
function rejectedFiles(event) {
    var eventID = $(event).attr("data-id");
    eventID = "download_files_" + eventID;
    document.getElementById(eventID).classList.toggle("show");
}

function resetAllfilter() {
    GROUP_NAME.val('');
    LEGAL_ENTITY_VAL.val('');
    DOMAIN_VAL.val('');
    UNIT_VAL.val('');
    TBODY_USERMAPPING_DETAILS.empty();
    REPORT_VIEW.hide();
    DETAILS.hide();
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
$(function() {
    bu.getLoadConstants();
    REPORT_VIEW.hide();
    initialize();
    fetchData();
    pageControls();
});