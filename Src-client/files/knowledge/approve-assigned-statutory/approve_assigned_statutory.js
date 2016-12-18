/* Elements */
var CancelButton = $('#btn-user-cancel');
var AssignStatutoryView = $("#assignstatutory-view");
var AssignStatutoryAdd = $("#assignstatutory-add");
var SubmitButton = $("#btn-submit");

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

/* Data */

var COMPLIANCES_LIST = null;
var ASSIGNED_STATUTORIES = null;

/* Values */
var val_group_id = null;
var val_legal_entity_id = null;
var val_domain_id = null;
var val_unit_id = null;
var ACTIVE_UNITS = [];
var CLIENT_STATUTORY_ID = null;

var LastAct='';
var LastSubAct='';
var statutoriesCount;
var actCount;


function loadSingleUnitCompliances() {
    var ccount = 1;
    var count = 1;
    statutoriesCount = 1;
    actCount = 1;
    AssignStatutoryList.empty();
    var sno = 0;
    $.each(COMPLIANCES_LIST, function(key, value) {
        if(LastAct != value.level_1_s_name){
            var acttableRow = $('#act-templates .p-head');
            var clone = acttableRow.clone();

            $('.acc-title', clone).attr('id', 'heading'+actCount);
            $('.panel-title a span', clone).text(value.level_1_s_name);
            $('.panel-title a', clone).attr('href', '#collapse'+actCount);
            $('.panel-title a', clone).attr('aria-controls', 'collapse'+actCount);

            $('.coll-title', clone).attr('id', 'collapse'+actCount);
            $('.coll-title', clone).attr('aria-labelledb', 'heading'+actCount);
            
            $('.change_status', clone).attr('id', 'act'+actCount);
            $('.change_status', clone).val(actCount);
            
            $('.remarks', clone).attr('id', 'remark'+actCount);
            $('.tbody-assignstatutory').append(clone);

            if(value.a_status == 2){
                $('#act'+actCount).html('<img src="images/deletebold.png">').attr('for','2');
                $('#remark'+ actCount).val(value.remarks);
                $('#remark' + actCount).show();
            }else if(value.a_status == 3){
                $('#act'+actCount).html('<img src="images/iconminusactive.png">').attr('for','3');
                $('#remark'+ actCount).val(value.remarks);
                $('#remark' + actCount).show();
            }else{
                $('#act'+actCount).html('<img src="images/tick1bold.png">').attr('for','1');
            }

            $('#act'+actCount).click(function() {
            if($(this).attr('for') == "1") {
              $(this).html('<img src="images/deletebold.png">').attr('for','2');
            } else if($(this).attr('for') == "2") {
              $(this).html('<img src="images/iconminusactive.png">').attr('for','3');
            } else {
              $(this).html('<img src="images/tick1bold.png">').attr('for','1');
            }
            actstatus(this);
        });

        ccount = actCount;
        LastAct = value.level_1_s_name;
        LastSubAct = value.level_1_s_name;
        actCount = actCount + 1;
        }
        ++sno;

        if(LastSubAct != value.map_text){
            var subTitleRow = $('#statutory-value .table-statutory-values .sub-title-row');
            var clone3 = subTitleRow.clone();
            $('.sub-title', clone3).text(value.map_text);
            $(' #collapse'+ccount+' .tbody-compliance-list').append(clone3);
            LastSubAct = value.map_text;
        }
        
        var complianceDetailtableRow = $('#statutory-value .table-statutory-values .compliance-details');
        var clone2 = complianceDetailtableRow.clone();
        var combineId = value.comp_id + '#' + value.level_1_s_id + '#' + value.u_id;
        $('.combineid-class', clone2).attr('id', 'combineid'+statutoriesCount);
        $('.combineid-class', clone2).val(combineId);

        $('.sno', clone2).text(statutoriesCount);
        $('.statutoryprovision', clone2).text(value.s_provision);
        $('.compliancetask', clone2).text(value.comp_name);
        $('.org-name', clone2).attr('title', 'Organizations: ' + value.org_names);
        $('.compliancedescription', clone2).text(value.descrip);

        $('.compliance-ck-box-1', clone2).attr('name', 'statutory' + statutoriesCount);
        $('.compliance-ck-box-1', clone2).attr('id', 'tick' + statutoriesCount);
        $('.compliance-ck-box-1', clone2).val(1);
        $('.compliance-ck-box-1', clone2).addClass('statutoryclass' + ccount);
        $('.compliance-label-1', clone2).attr('for', 'tick' + statutoriesCount);

        $('.compliance-ck-box-2', clone2).attr('name', 'statutory' + statutoriesCount);
        $('.compliance-ck-box-2', clone2).attr('id', 'untick' + statutoriesCount);
        $('.compliance-ck-box-2', clone2).val(2);
        $('.compliance-ck-box-2', clone2).addClass('statutoryclass' + ccount);
        $('.compliance-label-2', clone2).attr('for', 'untick' + statutoriesCount);

        $('.compliance-ck-box-3', clone2).attr('name', 'statutory' + statutoriesCount);
        $('.compliance-ck-box-3', clone2).attr('id', 'minus' + statutoriesCount);
        $('.compliance-ck-box-3', clone2).val(3);
        $('.compliance-ck-box-3', clone2).addClass('statutoryclass' + ccount);
        $('.compliance-label-3', clone2).attr('for', 'minus' + statutoriesCount);

        $('.saved', clone2).attr('id', 'save'+statutoriesCount);
        if(value.comp_status > 0){
            $('.saved', clone2).addClass('fa-square');
        }

        $('.comp', clone2).on('click', function () {
            compliancestatus(this);
        });
        
        $('.remarks').on('input', function (e) {
          this.value = isCommon($(this));
        });
    
        $(' #collapse'+ccount+' .tbody-compliance-list').append(clone2);

        if(value.comp_status > 0){
            if(value.comp_status == 1){
                $('#tick'+statutoriesCount).prop('checked', true);
            }else if(value.comp_status == 2){
                $('#untick'+statutoriesCount).prop('checked', true);
            }else{
                $('#minus'+statutoriesCount).prop('checked', true);
            }
        }
        statutoriesCount++;
        count++;
    });
    if(sno <= 0){
        SubmitButton.hide();
        SaveButton.hide();
    }else{
        SubmitButton.show();
        SaveButton.show();
    }
}


function EditAssignedStatutory(u_id, d_id){
    AssignStatutoryView.hide();
    AssignStatutoryAdd.show();
    mirror.getAssignedStatutoriesById(u_id, d_id, function(error, data) {
        if (error == null) {
            COMPLIANCES_LIST = data.statutories_for_assigning;
            loadCompliances();
        } else {
            custom_alert(error);
        }
    });
}

function loadAssignedStatutories(){
    var sno = 0;
    ACTIVE_UNITS = [];

    AssignedStatutoryList.empty();
    $.each(ASSIGNED_STATUTORIES, function(key, value){
        ++ sno;
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
        
        $('.view-icon', clone).on('click', function () {
            val_domain_id = value.d_id.toString();
            CLIENT_STATUTORY_ID = value.client_statutory_id;
            EditAssignedStatutory(value.u_id, value.d_id);
        });
        AssignedStatutoryList.append(clone);       
    });
}


SubmitButton.click(function(){
            var submission_status;
        if(api_type == SAVE_API){
            submission_status = 1;
        }else{
            submission_status = 2;
        }
        
        statutorysetting = [];
        var totalCompliance = 1;
        var checkSubmit = true;
        for(var i=1; i<=(actCount-1); i++){
            var aStatus = parseInt($('#act'+i).attr("for"));
            var remark = null;

            if(aStatus == 2 || aStatus==3){
                remark = $('#remark'+i).val().trim();
                if(remark==''){
                    displayMessage(message.act_remarks_required);
                    return false;
                }
            }

            var actComplianceCount = $('.statutoryclass'+i).length / 3;
            for(var j=1; j<=actComplianceCount; j++){
                var complianceStatusVal = 0;
                if($('input[name=statutory'+totalCompliance+']:checked').val() != undefined){
                    complianceStatusVal = parseInt($('input[name=statutory'+totalCompliance+']:checked').val());
                }else{
                    checkSubmit = false;
                }

                var combineidVal = $('#combineid'+totalCompliance).val().split('#');
                var comp_id = parseInt(combineidVal[0]);
                var level_1_s_id = parseInt(combineidVal[1]);
                var u_id = parseInt(combineidVal[2]);;
                
                if(CLIENT_STATUTORY_ID == null){
                    CLIENT_STATUTORY_ID = UNIT_CS_ID[u_id].client_statutory_id;
                }
                statutorysettingData = mirror.saveComplianceStatus(
                    int(val_group_id), int(val_legal_entity_id), u_id, 
                    int(val_domain_id), comp_id, complianceStatusVal,
                    level_1_s_id, aStatus, remark, CLIENT_STATUTORY_ID
                );
                statutorysetting.push(statutorysettingData);
                totalCompliance++;
            }
        }

        if(submission_status == 2 && checkSubmit == false){
            displayMessage(message.assigncompliance_submit_failure);
            return false;
        }else{
            mirror.saveAssignedStatutory(statutorysetting, submission_status, 
                function(error, data) {
                    if (error == null) {
                        displaySuccessMessage(message.save_success);
                        CLIENT_STATUTORY_ID = null;
                        showList();
                    } else {
                        custom_alert(error);
                    }
                }
            );
        }
});

function initialize() {
    AssignStatutoryView.show();
    AssignStatutoryAdd.hide();
    mirror.getAssignedStatutories(function(error, data) {
        if (error == null) {
            ASSIGNED_STATUTORIES = data.assigned_statutories;
            loadAssignedStatutories();
        } else {
            custom_alert(error);
        }
    });
}

$(function() {
    initialize();
    $(document).find('.js-filtertable').each(function(){
        $(this).filtertable().addFilter('.js-filter');
    });
});