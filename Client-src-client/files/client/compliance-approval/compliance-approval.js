var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var txtUnit = $('#txtUnit');
var hdnUnit = $('#hdnUnit');
var divUnit = $('#divUnit');

var ShowButton = $(".btn-show");

var approvalList;
var file_list = [];
var unitList = [];
var action;
var currentDate;
var sno = 0;
var totalRecord;
var lastAssignee;

var LE_ID = null;

function displayLoader() {
    $('.loading-indicator-spin').show();
}

function hideLoader() {
    $('.loading-indicator-spin').hide();
}

function initialize() {
    sno = 0;
    lastAssignee = '';
    displayLoader();
    LE_ID = parseInt(LegalEntityId.val());

    function onSuccess(data) {
        closeicon();
        $('.tbody-compliance-approval-list tr').remove();
        sno = 0;
        approvalList = data.approval_list;
        currentDate = data.current_date;
        totalRecord = data.total_count;
        loadComplianceApprovalDetails(approvalList);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
    client_mirror.getComplianceApprovalList(parseInt(LegalEntityId.val()), unit_id, sno,
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
}
$('#pagination').click(function() {
    displayLoader();
    $('.js-filter').val('');

    function onSuccess(data) {
        closeicon();
        approvalList = data.approval_list;
        currentDate = data.current_date;
        totalRecord = data.total_count;
        loadComplianceApprovalDetails(approvalList);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
    client_mirror.getComplianceApprovalList(parseInt(LegalEntityId.val()), unit_id, sno,
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
});
var unitName = "";
var lastAssignee = "";

function loadComplianceApprovalDetails(data) {
    $.each(data, function(key, val) {
        if (unitName != val.unit_name) {
            var cloneunit = $('#templates .table-compliance-approval-list .unitheadingRow').clone();
            $('.unit-name', cloneunit).html(val.unit_name);
            $('.tbody-compliance-approval-list').append(cloneunit);
            unitName = val.unit_name;
            lastAssignee = "";
        }

        if (lastAssignee != val.assignee_name) {
            var tableRowHeading = $('#templates .table-compliance-approval-list .headingRow');
            var clone = tableRowHeading.clone();
            $('.user-name', clone).html(val.assignee_name);
            $('.tbody-compliance-approval-list').append(clone);
            lastAssignee = val.assignee_name;
        }

        var tableRowvalues = $('#templates .table-compliance-approval-list .table-row-list');
        var clonelist = tableRowvalues.clone();
        sno = sno + 1;
        $('.sno-ca', clonelist).html(sno);
        // $('.compliance-task span', clonelist).html(val.compliance_name);
        $('.compliance-task span', clonelist).html(val.compliance_name + ' - ' + val.compliance_history_id);
        $('.compliance-task i', clonelist).attr('title', val.description);
        $('.domain', clonelist).html(val.domain_name);
        $('.startdate', clonelist).html(val.start_date);
        $('.duedate', clonelist).html(val.due_date);
        if (val.delayed_by == null) {
            $('.delayedby', clonelist).html('');
        }
        if (val.delayed_by != null) {
            $('.delayedby', clonelist).html(val.delayed_by);
            if ((val.delayed_by).indexOf("Overdue") > -1) {
                $('.delayedby', clonelist).addClass("text-danger");
            }
        }

        if (val.concurrence_status == '3') {
            $('.sno-ca', clonelist).html(sno);
            $('.compliance-task span', clonelist).addClass("text-danger");
            $('.domain', clonelist).addClass("text-danger");
            $('.startdate', clonelist).addClass("text-danger");
            $('.duedate', clonelist).addClass("text-danger");
            $('.delayedby', clonelist).addClass("text-danger");
        }

        var compliance_history_id = val.compliance_history_id;
        $(clonelist, '.expand-compliance').on('click', function() {
            clearMessage();
            $('.table-row-list').removeClass('active1');
            $(clonelist, '.table-row-list').addClass('active1');
            showSideBar(compliance_history_id, val);
        });
        $('.full-width-list .tbody-compliance-approval-list').append(clonelist);
    });
    $('[data-toggle="tooltip"]').tooltip();
    if (data.length == 0) {
        var norecordtableRow = $('#no-record-templates .table-no-content .table-row-no-content');
        var noclone = norecordtableRow.clone();
        $('.no_records', noclone).text('No Compliance Available');
        $('.tbody-compliance-approval-list').append(noclone);
        $('#pagination').hide();
        $('.compliance_count').text('');
    } else {
        $('.compliance_count').text('Total Compliances : ' + totalRecord);
        if (sno >= totalRecord) {
            $('#pagination').hide();
        } else {
            $('#pagination').show();
        }
    }
}

function getCountryId(le_id) {
    var c_id = null;
    $.each(LEGAL_ENTITIES, function(k, v) {
        if (v.le_id == parseInt(le_id)) {
            console.log("parseInt--" + v.c_id);
            c_id = v.c_id;
        }
    });
    return c_id;
}



function showSideBar(idval, data) {
    var fileslist = [];
    var documentslist = [];
    $('.half-width-task-details').empty();
    $('.half-width-task-details').show();
    $('.full-width-list').attr('width', '60%');
    $('.half-width-task-details').attr('width', '40%');
    //SideView append ---------------------------------------------------------------------
    var tableRowSide = $('#templates .sideview-div');
    var cloneValSide = tableRowSide.clone();
    var complianceFrequency = data.compliance_task_frequency;
    $('.validityAndDueDate', cloneValSide).hide();
    $('.sidebar-unit span', cloneValSide).html(data.unit_name);
    $('.sidebar-unit i', cloneValSide).attr('title', data.unit_address);
    // $('.sidebar-unit abbr', cloneValSide).attr("title", data['address']);
    $('.sidebar-compliance-task span', cloneValSide).html(data.compliance_name);
    $('.sidebar-compliance-task i', cloneValSide).attr('title', data.description);
    $('.sidebar-compliance-frequency', cloneValSide).html(complianceFrequency);
    fileslist = data.file_names;
    documentslist = data.uploaded_documents;
    if (documentslist != null) {
        for (var i = 0; i < documentslist.length; i++) {
            if (documentslist[i] != '') {
                $(".view-file", cloneDown).attr("title", data.uploaded_documents[i]);
                $(".download-file", cloneDown).attr("title", data.uploaded_documents[i]);
                var tableDown = $('#templates .temp-download');
                var cloneDown = tableDown.clone();
                $(".sidebardocview", cloneDown).html(documentslist[i]);
                $(".view-file", cloneDown).on("click", function() {
                    var getfilename = $(this).attr("title");
                    console.log(getfilename);
                    var file_ext = getfilename.slice(-3);
                    if (file_ext == "pdf") {
                        client_mirror.downloadTaskFile(LE_ID, getCountryId(LE_ID), data['domain_id'], data['unit_id'], data['start_date'], getfilename);
                    } else {
                        client_mirror.downloadTaskFile(LE_ID, getCountryId(LE_ID), data['domain_id'], data['unit_id'], data['start_date'], getfilename);
                    }

                });
                $(".download-file", cloneDown).on("click", function() {
                    var getfilename = $(this).attr("title");
                    client_mirror.downloadTaskFile(LE_ID, getCountryId(LE_ID), data['domain_id'], data['unit_id'], data['start_date'], getfilename);
                });

                $('.sidebar-uploaded-documents', cloneValSide).append(cloneDown);
                $('.tr-sidebar-uploaded-date', cloneValSide).show();
            }
        }
    }

    if (fileslist == null) {
        $('.sidebar-uploaded-documents', cloneValSide).val('-');
    }
    if (data.upload_date != null)
        $('.sidebar-uploaded-date', cloneValSide).html(data.upload_date);
    $('.sidebar-completion-date', cloneValSide).html(data.completion_date);
    if (complianceFrequency != 'One Time') {
        $('.validitydate1_textbox', cloneValSide).hide();
        $('.validitydate1_label', cloneValSide).show();
        $('.duedate1_textbox', cloneValSide).hide();
        $('.duedate1_label', cloneValSide).show();
        $('.validityAndDueDate', cloneValSide).show();
        $('.validitydate1_label', cloneValSide).html(data.validity_date);
        $('.duedate1_label abbr ', cloneValSide).html(data.next_due_date);
        $('.validity1-textbox-input', cloneValSide).val(data.validity_date);
        $('.duedate1-textbox-input', cloneValSide).val(data.next_due_date);
        $('.duedate1_icon', cloneValSide).on('click', function(e, data) {
            showTextbox();
        });
    }
    if (complianceFrequency == 'On Occurrence') {
        $('.validityAndDueDate', cloneValSide).hide();
    }
    // if (data.delayed_by != null) {
    //     $('.sidebar-status', cloneValSide).html('Not Complied');
    // }
    // if (data.delayed_by == null) {
    //     $('.sidebar-status', cloneValSide).html('InProgress');
    // }
    if (data.action == 'Concur') {
        $('.sidebar-status', cloneValSide).html('Submitted');
    } else if (data.action == 'Approve') {
        if (data.concurrence_status == '3') {
            $('.sidebar-status', cloneValSide).html('Concurred - Rejected');
        } else if (data.concurrence_status == '0') {
            $('.sidebar-status', cloneValSide).html('Submitted');
        } else {
            $('.sidebar-status', cloneValSide).html('Concurred');
        }

    } else {
        $('.sidebar-status', cloneValSide).html(data.action);
    }

    if (data.remarks != 'None') {
        $('.sidebar-remarks span', cloneValSide).html(data.remarks);
    }
    action = data.action;
    if (action == 'Approve') {
        $('.action-tr', cloneValSide).show();
        $('.concurr-action', cloneValSide).hide();
        $('.approval-action', cloneValSide).show();
        if (data.concurrenced_by != null) {
            $('.concurrance-tab', cloneValSide).show();
            $('.sidebar-concurrence span', cloneValSide).html(data.concurrenced_by);
        }
        $('.approval-action', cloneValSide).on('change', function(e, data) {
            if ($('.approval-action', cloneValSide).val() == 'Reject') {
                $('.sidebar-remarks-textarea', cloneValSide).val();
            } else if ($('.approval-action', cloneValSide).val() == 'Reject Approval') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else if ($('.approval-action', cloneValSide).val() == 'Rectify Approval') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else if ($('.concurr-action option:selected', cloneValSide).val() == 'Rectify Concurrence') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else if ($('.concurr-action option:selected', cloneValSide).val() == 'Reject Concurrence') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else {
                $('.sidebar-remarks-textarea', cloneValSide).hide();
            }
        });
    }
    if (action == 'Concur') {
        //$(".concurrance-tab", cloneValSide).show();
        $('.concurr-action', cloneValSide).show();
        $('.approval-action', cloneValSide).hide();
        //$(".sidebar-concurrence span", cloneValSide).html(data['concurrenced_by']);
        $('.action-tr', cloneValSide).show();
        $('.concurr-action', cloneValSide).on('change', function(e, data) {
            if ($('.concurr-action option:selected', cloneValSide).val() == 'Reject Concurrence') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else if ($('.concurr-action option:selected', cloneValSide).val() == 'Rectify Concurrence') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else {
                $('.sidebar-remarks-textarea', cloneValSide).hide();
            }
        });
    }
    if (action == 'Reject Concurrence' || action == "Rectify Concurrence") {
        $('.concurrance-tab', cloneValSide).show();
        $('.sidebar-concurrance', cloneValSide).html(data.remarks);
        $('.action-tr', cloneValSide).show();
        $('.concurr-action', cloneValSide).show();
        $('.approval-action', cloneValSide).hide();
        $('.sidebar-remarks-textarea', cloneValSide).show();
        $('.concurr-action', cloneValSide).on('change', function(e, data) {
            if ($('.concurr-action option:selected', cloneValSide).val() == 'Reject Concurrence') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else if ($('.concurr-action option:selected', cloneValSide).val() == 'Rectify Concurrence') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else {
                $('.sidebar-remarks-textarea', cloneValSide).hide();
            }
        });
    }
    if (action == 'Reject Approval' || action == "Rectify Approval") {
        $('.action-tr', cloneValSide).show();
        $('.concurr-action', cloneValSide).hide();
        $('.approval-action', cloneValSide).show();
        $('.sidebar-remarks-textarea', cloneValSide).show();
        $('.approval-action', cloneValSide).on('change', function(e, data) {
            if ($('.approval-action option:selected', cloneValSide).val() == 'Reject') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else if ($('.concurr-action option:selected', cloneValSide).val() == 'Rectify Concurrence') {
                $('.sidebar-remarks-textarea', cloneValSide).show();
            } else {
                $('.sidebar-remarks-textarea', cloneValSide).hide();
            }
        });
    }
    $(function() {
        $('.validity1-textbox-input', cloneValSide).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: 'dd-M-yy',
            monthNames: [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ]
        });
        $('.duedate1-textbox-input', cloneValSide).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: 'dd-M-yy',
            monthNames: [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ]
        });
    });

    function parseMyDate(s) {
        return new Date(s.replace(/^(\d+)\W+(\w+)\W+/, '$2 $1 '));
    }
    $('.btn-submit', cloneValSide).on('click', function(e) {
        var compliance_history_id;
        var approval_status;
        var remarks = '';
        var next_due_date;
        var validity_date;
        compliance_history_id = data.compliance_history_id;
        validity_settings_days = data.validity_settings_days;

        if (action == 'Concur') {
            approval_status = $('.concurr-action option:selected').val();
        }
        if (action == 'Reject Concurrence') {
            approval_status = $('.concurr-action option:selected').val();
        }
        if (action == 'Rectify Concurrence') {
            approval_status = $('.concurr-action option:selected').val();
        }
        if (action == 'Approve') {
            approval_status = $('.approval-action option:selected').val();
        }
        if (action == 'Reject Approval') {
            approval_status = $('.approval-action option:selected').val();
        }
        if (action == 'Rectify Approval') {
            approval_status = $('.approval-action option:selected').val();
        }

        //console.log(approval_status);
        var rem = $('.remarks-textarea', cloneValSide);
        if (approval_status == '') {
            displayMessage(message.action_required);
            return false;
        } else if (approval_status == 'Reject Concurrence') {
            if (isNotEmpty(rem, message.remarks_required) == false)
                return false;
            remarks = $('.remarks-textarea', cloneValSide).val();
        } else if (approval_status == 'Reject Approval') {
            if (isNotEmpty(rem, message.remarks_required) == false)
                return false;
            remarks = $('.remarks-textarea', cloneValSide).val();
        } else if (approval_status == 'Rectify Concurrence') {
            if (isNotEmpty(rem, message.remarks_required) == false)
                return false;
            remarks = $('.remarks-textarea', cloneValSide).val();
        } else if (approval_status == 'Rectify Approval') {
            if (isNotEmpty(rem, message.remarks_required) == false)
                return false;
            remarks = $('.remarks-textarea', cloneValSide).val();
        } else {
            remarks = data.remarks;
        }

        next_due_date = $('.duedate1-textbox-input', cloneValSide).val();
        validity_date = $('.validity1-textbox-input', cloneValSide).val();
        if (validity_date == '') {
            validity_date = $('.validitydate1_label', cloneValSide).html();
            if (validity_date == '') {
                validity_date = null;
            }
        } else {
            if (validity_settings_days != 0) {
                var convertDue = convert_date(next_due_date);
                var convertValidity = convert_date(validity_date);

                if (Math.abs(daydiff(convertDue, convertValidity)) <= validity_settings_days) {} else {
                    displayMessage(message.validity_date_before_after.replace('V_DAYS', validity_settings_days));
                    hideLoader();
                    return false;
                }
            }
        }

        if (next_due_date == '') {
            next_due_date = $('.duedate1_label abbr', cloneValSide).html();
            if (next_due_date == '') {
                next_due_date = null;
            }
        }

        if (currentDate != null && next_due_date != null) {
            if (parseMyDate(currentDate) > parseMyDate(next_due_date)) {
                displayMessage(message.nextduedate_gt_current);
                return;
            }
        }

        if ($('.remarks-textarea', cloneValSide).val().trim().length > 500) {
            displayMessage('Remarks' + message.should_not_exceed + ' 500 characters');
            return false;
        }
        if (remarks == '') {
            remarks = null;
        } else if (typeof remarks == 'undefined') {
            remarks = null;
        } else if (validity_date == '') {
            displayMessage(message.validitydate_required);
            return;
        } else if (next_due_date == '') {
            displayMessage(message.nextduedate_required);
            return;
        }
        // if (validity_date != null && next_due_date != null) {
        //     if (parseMyDate(next_due_date) > parseMyDate(validity_date)) {
        //         displayMessage(message.validitydate_gt_duedate);
        //         return;
        //     }
        // }


        displayLoader();

        function onSuccess(data) {
            clearMessage();
            if (approval_status == 'Reject Concurrence') {
                displaySuccessMessage(message.compliance_concur_reject);
            } else if (approval_status == 'Reject Approval') {
                displaySuccessMessage(message.compliance_app_reject);
            } else if (approval_status == 'Approve') {
                displaySuccessMessage(message.compliance_approval);
            } else if (approval_status == 'Concur') {
                displaySuccessMessage(message.compliance_concurred);
            } else if (approval_status == 'Rectify Approval') {
                displaySuccessMessage(message.compliance_rectify);
            } else if (approval_status == 'Rectify Concurrence') {
                displaySuccessMessage(message.compliance_rectify);
            }
            initialize();
            hideLoader();
        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }
        client_mirror.approveCompliance(parseInt(LegalEntityId.val()), compliance_history_id, [approval_status], remarks, next_due_date, validity_date, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    });
    $('.half-width-task-details').append(cloneValSide);
    $('.remarks-textarea').on('input', function(e) {
        this.value = isCommon($(this));
    });
}

function showTextbox() {
    $('.validitydate1_textbox').show();
    $('.validitydate1_label').hide();
    $('.duedate1_textbox').show();
    $('.duedate1_label').hide();
}

function hideTextbox() {
    $('.validitydate1_textbox').hide();
    $('.validitydate1_label').show();
    $('.duedate1_textbox').hide();
    $('.duedate1_label').show();
}

function closeicon() {
    $('.half-width-task-details').hide();
    $('.full-width-list').attr('width', '100%');
    $('.half-width-task-details').attr('width', '0%');
}

function uploadedfile(e) {}

function remove_temp_file(classnameval) {
    $('.' + classnameval).remove();
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    if (id_element[0].id == 'legal_entity_id') {
        loadUnits(parseInt(LegalEntityId.val()));
    }
}

function loadUnits(le_id, unit_id) {
    client_mirror.complianceFilters(le_id, function(error, response) {
        if (error == null) {
            unitList = response.user_units;
        }
    });
}

ShowButton.click(function() {
    if (LegalEntityId.val().trim().length <= 0) {
        displayMessage(message.legalentity_required);
        return false;
    } else {
        initialize();
    }
});

LegalEntityName.keyup(function(e) {
    var text_val = $(this).val();
    commonAutoComplete(
        e, ACLegalEntity, LegalEntityId, text_val,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
        });
});

//Unit Auto Complete
txtUnit.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    var text_val = $(this).val();
    commonAutoComplete(
        e, divUnit, hdnUnit, text_val,
        unitList, "unit_name", "unit_id",
        function(val) {
            onAutoCompleteSuccess(txtUnit, hdnUnit, val);
        }, condition_fields, condition_values);
});

function loadEntityDetails() {
    if (LEGAL_ENTITIES.length > 1) {
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();

        var norecordtableRow = $('#no-record-templates .table-no-content .table-row-no-content');
        var noclone = norecordtableRow.clone();
        $('.no_records', noclone).text('No Compliance Available');
        $('.tbody-compliance-approval-list').append(noclone);
        $('#pagination').hide();
        $('.compliance_count').text('');

    } else {
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        loadUnits(parseInt(LegalEntityId.val()));
        ShowButton.trigger("click");
    }
}

$(function() {
    loadEntityDetails();
});

$(document).find('.js-filtertable').each(function() {
    $(this).filtertable().addFilter('.js-filter');
});

// $(document).tooltip({
//     position: {
//         my: 'center bottom-20',
//         at: 'center top',
//         using: function(position, feedback) {
//             $(this).css(position);
//             $('<div>').addClass('arrow').addClass(feedback.vertical).addClass(feedback.horizontal).appendTo(this);
//         }
//     }
// });