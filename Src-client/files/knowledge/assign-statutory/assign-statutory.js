/* Elements */
var CURRENT_TAB = 1;
var AddButton = $(".btn-assignstatutory-add");
var CancelButton = $('#btn-user-cancel');
var AssignStatutoryView = $("#assignstatutory-view");
var AssignStatutoryAdd = $("#assignstatutory-add");
var Show = $(".btn-show");
var NextButton = $('#btn-next');
var PreviousButton = $('#btn-previous');
var SubmitButton = $("#btn-submit");
var SaveButton = $("#btn-save");


var GroupName = $('#group_name');
var GroupId = $("#group_id");
var ACGroup = $("#ac-group");

var BusinessGroupName = $("#business_group_name");
var BusinessGroupId = $("#business_group_id");
var ACBusinessGroup = $("#ac-business-group");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var DivisionName = $("#division_name");
var DivisionId = $("#division_id");
var ACDivision = $("#ac-division");

var CategoryName = $("#category_name");
var CategoryId = $("#category_id");
var ACCategory = $("#ac-category");

var DomainName = $("#domain_name");
var DomainId = $("#domain_id");
var ACDomain = $("#ac-domain");

var UnitRow = $("#templates .unit-row li");
var UnitList = $(".unit-list");
var SelectAll = $('.select_all');
var SelectedUnitCount = $(".selected_checkbox_count");

var BreadCrumbs = $(".breadcrumbs");
var BreadCrumbImg = '<i class="fa fa-angle-double-right"></i>';

var AssignStatutoryList = $(".tbody-assignstatutory");
var SNo = ".sno";
var StatutoryProvision = ".statutoryprovision";
var ComplianceTask = ".compliancetask";
var ComplianceDescription = ".compliancedescription";

var AssignedStatutoryList = $(".tbody-assignstatutory-list");
var AssignedStatutoryRow = $("#templates .table-assignstatutory .table-row");

var TblSno = ".tbl_sno";
var TblCountry = ".tbl_country";
var TblGroup = ".tbl_group";
var TblBG = ".tbl_businessgroup";
var TblLE = ".tbl_legalentity";
var TblDiv = ".tbl_division";
var TblCat = ".tbl_category";
var TblLoc = ".tbl_location";
var TblUnit = ".tbl_unit";
var TblDomain = ".tbl_domain";
var TblStatus = ".tbl_status";
var TblEditIcon = ".edit-icon";

/* Data */
var GROUPS = null;
var BUSINESS_GROUPS = null;
var LEGAL_ENTITIES = null;
var DIVISIONS = null;
var CATEGORIES = null;
var UNITS = null;
var DOMAINS = null;
var COMPLIANCES_LIST = null;
var ASSIGNED_STATUTORIES = null;

/* Values */
var val_group_id = null;
var val_business_group_id = null;
var val_legal_entity_id = null;
var val_division_id = null;
var val_category_id = null;
var val_domain_id = null;
var val_unit_id = null;
var ACTIVE_UNITS = [];
var bred_crump_text = null;


/* API Types */
var API_Wizard1 = "wizard_1";
var API_Wizard2 = "wizard_2";
var SAVE_API = "save";
var SUBMIT_API = "submit";
var API_LIST = "list";
var EDIT_API = "edit"

var LastAct='';
var LastSubAct='';
var statutoriesCount;
var actCount;

function callAPI(api_type) {
    if (api_type == API_LIST){
        mirror.getAssignedStatutories(function(error, data) {
            if (error == null) {
                ASSIGNED_STATUTORIES = data.assigned_statutories;
                loadAssignedStatutories();
            } else {
                custom_alert(error);
            }
        });
    }
    else if (api_type == API_Wizard1) {
        mirror.getAssignStatutoryWizardOneData(function(error, data) {
            if (error == null) {
                GROUPS = data.grps;
                BUSINESS_GROUPS = data.bgrps;
                LEGAL_ENTITIES = data.lety;
                DIVISIONS = data.divs;
                CATEGORIES = data.cates;
                DOMAINS = data.dms;
            } else {
                custom_alert(error);
            }
        });
    }

    else if (api_type == API_Wizard2) {
        showBreadCrumbText();
        mirror.getAssignStatutoryWizardTwoData(
            int(val_domain_id), ACTIVE_UNITS,
            function(error, data) {
                if (error == null) {
                    COMPLIANCES_LIST = data.statutories_for_assigning;
                    loadCompliances();
                } else {
                    custom_alert(error);
                }
            }
        );
    }

    else if (api_type == SAVE_API || api_type == SUBMIT_API){

        var submission_status;
        if(api_type == SAVE_API){
            submission_status = 1;
        }else{
            submission_status = 2;
        }
        
        statutorysetting = [];
        var totalCompliance = 1;
       
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
                }

                var combineidVal = $('#combineid'+totalCompliance).val().split('#');
                var comp_id = parseInt(combineidVal[0]);
                var level_1_s_id = parseInt(combineidVal[1]);
                var u_id = 1;
                var client_statutory_id = null;
              
                
                statutorysettingData = mirror.saveComplianceStatus(
                    int(val_group_id), int(val_legal_entity_id), u_id, 
                    int(val_domain_id), comp_id, complianceStatusVal,
                    level_1_s_id, aStatus, remark, client_statutory_id
                );
                statutorysetting.push(statutorysettingData);
                totalCompliance++;
            }
        }
        mirror.saveAssignedStatutory(statutorysetting, submission_status, 
            function(error, data) {
                if (error == null) {
                    displayMessage(message.save_success);
                    CLIENT_STATUTORY_ID = null;
                    showList();
                } else {
                    custom_alert(error);
                }
            }
        );
    }
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
}

function pageControls() {
    NextButton.click(function() {
        CURRENT_TAB += 1;
        showTab();
    });
    PreviousButton.click(function() {
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
    });

    AddButton.click(function() {
        showTab();
        AssignStatutoryView.hide();
        AssignStatutoryAdd.show();
        callAPI(API_Wizard1);
    });

    CancelButton.click(function() {
        showList();
    });

    GroupName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, GroupId, text_val,
            GROUPS, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupName, GroupId, val);
            });
    });
    BusinessGroupName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACBusinessGroup, BusinessGroupId, text_val,
            BUSINESS_GROUPS, "business_group_name", "business_group_id",
            function(val) {
                onAutoCompleteSuccess(BusinessGroupName, BusinessGroupId, val);
            });
    });
    LegalEntityName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACLegalEntity, LegalEntityId, text_val,
            LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
            function(val) {
                onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
            });
    });
    DivisionName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDivision, DivisionId, text_val,
            DIVISIONS, "division_name", "division_id",
            function(val) {
                onAutoCompleteSuccess(DivisionName, DivisionId, val);
            });
    });
    CategoryName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACCategory, CategoryId, text_val,
            CATEGORIES, "category_name", "category_id",
            function(val) {
                onAutoCompleteSuccess(CategoryName, CategoryId, val);
            });
    });
    DomainName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomain, DomainId, text_val,
            DOMAINS, "domain_name", "domain_id",
            function(val) {
                onAutoCompleteSuccess(DomainName, DomainId, val);
            });
    });
    Show.click(function() {
        validateAndShow();
    });

    SubmitButton.click(function(){
        callAPI(SUBMIT_API);
    });
    
    SaveButton.click(function(){
        callAPI(SAVE_API);
    });

    SelectAll.click(function() {
        ACTIVE_UNITS=[];
        $('.unit-list li').each(function (index, el) {
            if(SelectAll.prop('checked')){
              $(el).addClass('active');
              $(el).find('i').addClass('fa fa-check pull-right');
              var chkid = parseInt($(el).attr('id'));
              ACTIVE_UNITS.push(chkid);
            }else{
              $(el).removeClass('active');
              $(el).find('i').removeClass('fa fa-check pull-right');
            }
        });
        SelectedUnitCount.text(ACTIVE_UNITS.length);
    });
    
}

function showBreadCrumbText() {
    BreadCrumbs.empty();
    var img_clone = BreadCrumbImg;
    BreadCrumbs.append(GroupName.val());

    if (BusinessGroupName.val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + BusinessGroupName.val() + " ");
    }

    BreadCrumbs.append(img_clone);
    BreadCrumbs.append(" " + LegalEntityName.val() + " ");

    if (DivisionName.val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + DivisionName.val() + " ");
    }

    if (CategoryName.val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + CategoryName.val() + " ");
    }

    if (DomainName.val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + DomainName.val() + " ");
    }
}

function int(val) {
    try {
        value = val.trim();
        value = parseInt(value);
        return value;
    } catch (e) {
        return null;
    }
}

function validateAndShow() {
    val_group_id = GroupId.val();
    val_legal_entity_id = LegalEntityId.val();
    val_domain_id = DomainId.val();

    val_division_id = DivisionId.val();
    val_category_id = CategoryId.val();
    val_business_group_id = BusinessGroupId.val();

    
    if (val_group_id.trim().length <= 0) {
        displayMessage(message.group_required);
        return false;
    } else if (val_legal_entity_id.trim().length <= 0) {
        displayMessage(message.legalentity_required);
        return false;
    } else if (val_domain_id.trim().length <= 0) {
        displayMessage(message.domain_required);
        return false;
    } else {
        mirror.getAssignStatutoryWizardOneDataUnits(int(val_group_id), int(val_business_group_id), 
            int(val_legal_entity_id), int(val_division_id), int(val_category_id), int(val_domain_id), 
            function(error, data) {
            if (error == null) {
                UNITS = data.statu_units;
                loadUnits();
            } else {
                custom_alert(error);
            }
        });
    }
}

function loadUnits() {
    UnitList.empty();
    $.each(UNITS, function(key, value) {
        unit_text = value.unit_code + " - " + value.u_name + " - " + value.address;
        var clone = UnitRow.clone();
        clone.html(unit_text + '<i></i>');
        clone.attr('id', value.u_id);
        UnitList.append(clone);
        clone.click(function() {
            activateUnit(this);
        });
    });
}

function activateUnit(element) {
    var chkstatus = $(element).attr('class');
    var chkid = parseInt($(element).attr('id'));
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
        index = ACTIVE_UNITS.indexOf(chkid)
        ACTIVE_UNITS.splice(index, 1);
    } else {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');
        ACTIVE_UNITS.push(chkid);
    }
    SelectedUnitCount.text(ACTIVE_UNITS.length);
}

//show/hide remark textbox based on act applicable selection
function actstatus(element) {
  var checkedVal = $(element).attr("for");
  var remarkbox = '#remark' + $(element).val();
  var changestatusStatutories = '.statutoryclass' + $(element).val();
  $(changestatusStatutories).each(function () {
    var cVal = $(this).val();
    if(checkedVal == cVal){
        $(this).prop("checked", true);
        if(checkedVal > 1){
            $(remarkbox).show();
        }else{
            $(remarkbox).hide();
        }
    }

    var sname = $(this).attr('name');
    var sid = sname.substr(sname.lastIndexOf('y') + 1);
    $('#save'+sid).addClass('fa-square');
  });
}

function compliancestatus(element) {
    var sname = $(element).attr('name');
    var sid = sname.substr(sname.lastIndexOf('y') + 1);
    $('#save'+sid).addClass('fa-square');


  /*var sClass = $(element).attr('class').split(' ')[2];
  var actSelect = sClass.substr(sClass.lastIndexOf('s') + 1);
  var cStatus = false;
  $('.' + sClass).each(function () {
    var checkedVal = $('input[name=statutory'+actSelect+']:checked').val();
    if (checkedVal != 2) {
      cStatus = true;
    }
  });

  if (cStatus) {
    $('#act'+actSelect).html('<img src="images/tick1bold.png">').attr('for','1');
    $('#remark' + actSelect).hide();
  } else {
    $('#act'+actSelect).html('<img src="images/deletebold.png">').attr('for','2');
    $('#remark' + actSelect).show();
  }*/
  
}

function loadCompliances() {
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

            if(value.a_status == 1){
                $('#act'+actCount).html('<img src="images/tick1bold.png">').attr('for','1');
            }else if(value.a_status == 2){
                $('#act'+actCount).html('<img src="images/deletebold.png">').attr('for','2');
                $('#remark'+ actCount).val(value.remarks);
                $('#remark' + actCount).show();
            }else{
                $('#act'+actCount).html('<img src="images/iconminusactive.png">').attr('for','3');
                $('#remark'+ actCount).val(value.remarks);
                $('#remark' + actCount).show();
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
        var combineId = value.comp_id + '#' + value.level_1_s_id;
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

function showList(){
    CURRENT_TAB = 1;
    AssignStatutoryView.show();
    AssignStatutoryAdd.hide();
    callAPI(API_LIST);
}

function ifNullReturnHyphen(value){
    if(value){
        return value;
    }else{
        return "-";
    }
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
        $(TblLoc, clone).text(value.g_name);
        $(TblUnit, clone).text(value.u_name);
        $(TblDomain, clone).text(value.d_name);
        var status_text = null;
        if(value.a_s_id == 1){
            status_text = "Yet to submit";
        }else if(value.a_s_id == 2){
            status_text = "Submitted";
        }else if(value.a_s_id == 3){
            status_text = "Rejected";
        }else if(value.a_s_id == 4){
            status_text = "Assigned";
        }
        $(TblStatus, clone).text(status_text);

        GroupName.val(value.grp_name);
        BusinessGroupName.val(value.b_grp_name);
        LegalEntityName.val(value.l_e_name);
        DivisionName.val(value.div_name);
        CategoryName.val(value.cat_name);
        DomainName.val(value.d_name);
        /*GroupId.val(value.client_id);
        val_group_id = value.client_id;
        BusinessGroupId.val(value.business_group_id);
        LegalEntityId.val(value.legal_entity_id);
        DivisionId.val(value.division_id);
        CategoryId.val(value.category_id);
        CLIENT_STATUTORY_ID = value.client_statutory_id;
        ACTIVE_UNITS.push(value.unit_id);*/

        $('.edit-icon', clone).on('click', function () {
           EditAssignedStatutory(value.u_id, value.d_id);
        });
        AssignedStatutoryList.append(clone);       
    });
}

function validateFirstTab() {
    if (ACTIVE_UNITS.length <= 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
        callAPI(API_Wizard2);
        return true;
    }
};

function showTab(){
    hideall = function() {
        // $('.setup-panel li').addClass('disabled');
        $('.statutory_mapping_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();
        SaveButton.hide();
        SubmitButton.hide();
        NextButton.hide();
        PreviousButton.hide();
    }

    enabletabevent = function(tab) {
        if (tab == 1) {
            $('.tab-step-1 a').attr('href', '#tab1');
        }
        else if (tab == 2) {
            $('.tab-step-2 a').attr('href', '#tab2');
        }
    }
    disabletabevent = function() {
        $('.tab-step-1 a').removeAttr('href');
        $('.tab-step-2 a').removeAttr('href');
    }

    if (CURRENT_TAB == 1) {
        hideall();
        disabletabevent();
        enabletabevent(1);
        $('.tab-step-1').addClass('active')
        $('#tab1').addClass("active in");
        $('#tab1').show();
        NextButton.show();        
    }
    else if (CURRENT_TAB == 2) {
        if(validateFirstTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        }
        hideall();
        enabletabevent(2);
        $('.tab-step-2').addClass('active')
        $('#tab2').addClass('active in');
        $('#tab2').show();
        SubmitButton.show();
        PreviousButton.show();
        SaveButton.show();
        showBreadCrumbText();
    }
};

function EditAssignedStatutory(u_id, d_id){
    AssignStatutoryView.hide();
    AssignStatutoryAdd.show();
    mirror.getAssignedStatutoriesById(u_id, d_id, function(error, data) {
        if (error == null) {
            COMPLIANCES_LIST = data.statutories_for_assigning;

            $('.statutory_mapping_tab li').removeClass('active');
            $('.tab-pane').removeClass('active in');
            $('#tab1').hide();
            SaveButton.hide();
            NextButton.hide();
            $('.tab-step-2 a').attr('href', '#tab2');
            $('.tab-step-2').addClass('active')
            $('#tab2').addClass('active in');
            $('#tab2').show();
            SubmitButton.show();
            PreviousButton.hide();
            showBreadCrumbText();
            loadCompliances();
        } else {
            custom_alert(error);
        }
    });
}
function initialize() {
    pageControls();
    showList();
}

$(function() {
    initialize();
});

$(document).ready(function() {
    $(document).find('.js-filtertable').each(function(){
        $(this).filtertable().addFilter('.js-filter');
    });
});


/*$('.statutory_mapping_tab li').click(function(e){
    alert($(e.target).parent().attr('class').hasClass("disabled"))
});*/