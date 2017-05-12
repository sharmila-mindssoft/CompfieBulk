/* Elements */
var CancelButton = $('#btn-user-cancel');
var AssignStatutoryView = $("#assignstatutory-view");
var AssignStatutoryAdd = $("#assignstatutory-add");
var SubmitButton = $("#btn-submit");
var ShowMore = $(".btn-showmore");
var PasswordSubmitButton = $('#password-submit');

var AssignStatutoryList = $(".tbody-assignstatutory");
var StatutoryProvision = ".statutoryprovision";
var ComplianceTask = ".compliancetask";
var ComplianceDescription = ".compliancedescription";

var AssignedStatutoryList = $(".tbody-approved-assigned-statutories-list");
var AssignedStatutoryRow = $("#templates .table-approved-assigned-statutories .table-row");

var TblSno = ".tbl_sno";
var TblCountry = ".tbl_country";
var TblGroup = ".tbl_group";
var TblBG = ".tbl_businessgroup";
var TblLE = ".tbl_legalentity";
var TblDiv = ".tbl_division";
var TblCat = ".tbl_category";
var TblUnit = ".tbl_unit";
var TblDomain = ".tbl_domain";
var TblStatus = ".tbl_status";
var TblView = ".view-icon";

var ApprovalStatus = $('#approval-status');
var CurrentPassword = $('#current-password');
var isAuthenticate;

/* Data */
var COMPLIANCES_LIST = null;
var ASSIGNED_STATUTORIES = null;

/* Values */

var DOMAIN_ID = null;
var UNIT_ID = null;
var REJ_COMP = [];
var CLIENT_STATUTORY_ID = null;
var UNIT_TEXT = null;
var DOMAIN_TEXT = null;
var GROUP_TEXT = null;
var LE_TEXT = null;
var BG_TEXT = null;

var LastAct = '';
var LastSubAct = '';
var statutoriesCount = 1;
var actCount = 1;
var count = 1;
var totalRecord = 0;

AssignStatutoryList.empty();


function loadCompliances() {
    $.each(COMPLIANCES_LIST, function(key, value) {
        if (LastAct != value.level_1_s_name) {
            var acttableRow = $('#act-templates .p-head');
            var clone = acttableRow.clone();

            $('.acc-title', clone).attr('id', 'heading' + actCount);
            $('.panel-title a span', clone).text(value.level_1_s_name);
            $('.panel-title a', clone).attr('href', '#collapse' + actCount);
            $('.panel-title a', clone).attr('aria-controls', 'collapse' + actCount);

            $('.coll-title', clone).attr('id', 'collapse' + actCount);
            $('.coll-title', clone).attr('aria-labelledb', 'heading' + actCount);

            if (value.a_status == 2) {
                $('.act-status', clone).html('<img src="images/deletebold.png">');
                $('.remarks', clone).val(value.remarks);
                $('.remarks-div abbr', clone).attr("data-original-title", value.remarks);
                $('.r-view', clone).show();
            } else if (value.a_status == 3) {
                $('.act-status', clone).html('<img src="images/iconminusactive.png">');
                $('.remarks', clone).val(value.remarks);
                $('.r-view', clone).show();
            } else {
                $('.act-status', clone).html('<img src="images/tick1bold.png">');
            }
            $('.tbody-assignstatutory').append(clone);

            count = actCount;
            LastAct = value.level_1_s_name;
            LastSubAct = '';
            actCount = actCount + 1;
        }

        if (LastSubAct != value.map_text) {
            var subTitleRow = $('#statutory-value .table-statutory-values .sub-title-row');
            var clone3 = subTitleRow.clone();
            $('.sub-title', clone3).text(value.map_text);
            $(' #collapse' + count + ' .tbody-compliance-list').append(clone3);
            LastSubAct = value.map_text;
        }

        var complianceDetailtableRow = $('#statutory-value .table-statutory-values .compliance-details');
        var clone2 = complianceDetailtableRow.clone();

        $('.sno', clone2).text(statutoriesCount);
        $('.statutoryprovision', clone2).text(value.s_provision);
        $('.compliancetask', clone2).text(value.comp_name);
        $('.org-name', clone2).attr('title', 'Organizations: ' + value.org_names);
        $('.compliancedescription', clone2).text(value.descrip);
        $('.rejected', clone2).on('click', function(event) {
            if ($(event.target).hasClass("text-muted") ||
                $(event.target).find('i').hasClass("text-muted")) {
                $(this).html('<i class="fa fa-square text-warning c-pointer"></i>');
                REJ_COMP.push(value.comp_id);
            } else {
                $(this).html('<i class="fa fa-square text-muted c-pointer"></i>');
                index = REJ_COMP.indexOf(value.comp_id);
                REJ_COMP.splice(index, 1);
            }
        });

        if (value.comp_status == 1) {
            $('.tick', clone2).html('<img src="images/tick1bold.png">');
        } else if (value.comp_status == 2) {
            $('.untick', clone2).html('<img src="images/deletebold.png">');
        } else {
            $('.minus', clone2).html('<img src="images/iconminusactive.png">');
        }

        $(' #collapse' + count + ' .tbody-compliance-list').append(clone2);
        statutoriesCount++;
    });

    if (totalRecord == (statutoriesCount - 1)) {
        SubmitButton.show();
        $(".action-view").show();
        ShowMore.hide();
    } else {
        SubmitButton.hide();
        $(".action-view").hide();
        ShowMore.show();
    }
    $(".total_count").text('Showing 1 to ' + (statutoriesCount - 1) + ' of ' + totalRecord + ' entries');
    $(".total_count_view").show();
    hideLoader();
}

function ifNullReturnHyphen(value) {
    if (value) {
        return value;
    } else {
        return "-";
    }
}

function callAPI() {
    displayLoader();
    mirror.getAssignedStatutoriesComplianceToApprove(
        DOMAIN_ID, UNIT_ID, (statutoriesCount - 1),
        function(error, data) {
            if (error == null) {
                COMPLIANCES_LIST = data.statutories_for_assigning;
                AssignStatutoryView.hide();
                AssignStatutoryAdd.show();
                loadCompliances();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
}

function EditAssignedStatutory(u_id, d_id) {
    displayLoader();
    callAPI();
}

//validate
function validateAuthentication() {
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    } 
    else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }
    displayLoader();
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            isAuthenticate = true;
            Custombox.close();
        } else {
            hideLoader();
            if(error == 'InvalidPassword'){
                displayMessage(message.invalid_password);
            }else{
                displayMessage(error);
            }
            
            CurrentPassword.val('');
            CurrentPassword.focus();
        }
    });
}

function loadAssignedStatutories() {
    var sno = 0;
    REJ_COMP = [];

    AssignedStatutoryList.empty();
    $.each(ASSIGNED_STATUTORIES, function(key, value) {
        ++sno;
        var clone = AssignedStatutoryRow.clone();
        $(TblSno, clone).text(sno);
        $(TblCountry, clone).text(value.c_name);
        $(TblGroup, clone).text(value.grp_name);
        $(TblBG, clone).text(value.b_grp_name);
        $(TblLE, clone).text(value.l_e_name);
        $(TblDiv, clone).text(ifNullReturnHyphen(value.div_name));
        $(TblCat, clone).text(ifNullReturnHyphen(value.cat_name));
        $(TblUnit, clone).text(value.u_name);
        $(TblDomain, clone).text(value.d_name);

        $('.view-icon', clone).on('click', function() {
            displayLoader();
            totalRecord = value.total_count;
            ApprovalStatus.val('');
            $('#reason').val('');
            LastAct = '';
            LastSubAct = '';
            statutoriesCount = 1;
            actCount = 1;
            count = 1;
            AssignStatutoryList.empty();
            $(".total_count_view").hide();

            REJ_COMP = [];
            DOMAIN_ID = value.d_id;
            UNIT_ID = value.u_id;
            CLIENT_STATUTORY_ID = value.client_statutory_id;
            UNIT_TEXT = value.u_name;
            DOMAIN_TEXT = value.d_name;
            GROUP_TEXT = value.grp_name;
            LE_TEXT = value.l_e_name;
            BG_TEXT= value.b_grp_name;
            EditAssignedStatutory(value.u_id, value.d_id);
        });
        AssignedStatutoryList.append(clone);
    });
    hideLoader();
}

ApprovalStatus.on('change', function() {
    if ($(this).val() == 4) {
        $(".reason-view").show();
    } else {
        $(".reason-view").hide();
    }
});

ShowMore.click(function() {
    callAPI();
});

SubmitButton.click(function() {
    displayLoader();
    var approval_status = ApprovalStatus.val();
    var reason = $('#reason').val().trim();

    if (approval_status.length <= 0) {
        hideLoader();
        displayMessage(message.action_required);
        return false;
    } else if (approval_status == 4 && REJ_COMP.length == 0) {
        hideLoader();
        displayMessage(message.no_compliance_to_reject);
        return false;
    } else if (approval_status == 4 && reason.trim().length <= 0) {
        hideLoader();
        displayMessage(message.remarks_required_rejection);
        return false;
    }else if (approval_status == 4 && validateMaxLength("remark", reason, "Reason") == false) {
        hideLoader();
        return false;
    } else {
        Custombox.open({
            target: '#custom-modal',
            effect: 'contentscale',
            complete: function() {
                CurrentPassword.focus();
                CurrentPassword.val('');
                isAuthenticate = false;
                hideLoader();
            },
            close: function() {
                if (isAuthenticate) {
                    mirror.approveAssignedStatutory(UNIT_ID, DOMAIN_ID, CLIENT_STATUTORY_ID, REJ_COMP,
                        parseInt(approval_status), reason, UNIT_TEXT, DOMAIN_TEXT, GROUP_TEXT, LE_TEXT, BG_TEXT,
                        function(error, data) {
                            if (error == null) {
                                $(".total_count_view").hide();
                                if(approval_status == 3){
                                    displaySuccessMessage(message.assign_statutory_approved_success);
                                }else{
                                    displaySuccessMessage(message.assign_statutory_rejected_success);
                                }
                                initialize();
                            } else {
                                hideLoader();
                                displayMessage(error);
                            }
                        }
                    );
                }
            },
        });
    }
});

PasswordSubmitButton.click(function() {
    validateAuthentication();
});

CancelButton.click(function() {
    AssignStatutoryView.show();
    AssignStatutoryAdd.hide();
});

function initialize() {
    displayLoader();
    AssignStatutoryView.show();
    AssignStatutoryAdd.hide();
    mirror.getAssignedStatutoriesForApprove(function(error, data) {
        if (error == null) {
            ASSIGNED_STATUTORIES = data.assigned_statutories_approve;
            loadAssignedStatutories();
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

$(function() {
    $('html').offset().top;
    initialize();
    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
    $(".table-fixed").stickyTableHeaders();
});
// $(function(){
//   $(".remarks-div abbr").tooltip({
//     customClass: 'custom-tooltip-class'
//   });
// });
