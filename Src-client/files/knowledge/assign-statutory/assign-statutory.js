/* Elements */
var AddButton = $(".btn-assignstatutory-add");
var CancelButton = $('#btn-user-cancel');
var AssignStatutoryView = $("#assignstatutory-view");
var AssignStatutoryAdd = $("#assignstatutory-add");

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

var Show = $(".btn-show");
var SelectedUnitCount = $(".selected_checkbox_count");
var ChangeAccordianHeaderStatus = ".change_status";

var ActivateStep2 = $("#activate-step-2");


var BreadCrumbs = $(".breadcrumbs");
var BreadCrumbImg = '<i class="fa fa-angle-double-right"></i>';


var AccordianHeader = $("#templates .compliances-accordian-header table");
var AssignStatutoryList = $(".tbody-assignstatutory");
var ACT_NAME = ".actname";
var StatutoryHeader = $("#templates #statutory-header tr");
var StatutoryValue = $("#templates #statutory-value tr")
var StatutoryValuesList = ".checkedtable";

var SNo = ".sno";
var StatutoryProvision = ".statutoryprovision";
var ComplianceTask = ".compliancetask";
var ComplianceDescription = ".compliancedescription";
var Applicable = ".applicable";
var NotApplicable = ".not-applicable";
var NotAtAllApplicable = ".not-at-all-applicable";
var IsSaved = ".saved";
var ApplicableActiveIcon = "applicable-active-icon";
var ApplicableInActiveIcon = "applicable-inactive-icon";
var NotApplicableActiveIcon = "not-applicable-active-icon";
var NotApplicableInActiveIcon = "not-applicable-inactive-icon";
var NotAtAllApplicableActiveIcon = "not-atall-applicable-active-icon";
var NotAtAllApplicableInActiveIcon = "not-atall-applicable-inactive-icon";
var SavedActiveIcon = "saved-active-icon";
var SavedInActiveIcon = "saved-inactive-icon";

var CURRENT_TAB = 1;
var NextButton = $('#btn-next');
var PreviousButton = $('#btn-previous');
var SubmitButton = $("#btn-submit");
var SaveButton = $("#btn-save");

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
var LEVEL_1_STATUTORIES = null;
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
var SELECTED_COMPLIANCES = {};
var LEVEL_1_STATUTORYWISE_COMPLIANCES = {}
var CLIENT_STATUTORY_ID = null;

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

    else if (api_type == EDIT_API){
        mirror.getAssignedStatutoriesById(CLIENT_STATUTORY_ID, function(error, data) {
            if (error == null) {
                LEVEL_1_STATUTORIES = data.level_1_statutories_list;
                COMPLIANCES_LIST = data.statutories_for_assigning;
                loadCompliances();
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
                //UNITS = data.unit_id_name;
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

    else if (api_type == SAVE_API){
        /*selected_compliances_list = [];
        $.each(SELECTED_COMPLIANCES, function(key, value){
            value["compliance_id"] = parseInt(key);
            selected_compliances_list.push(
                value
            );
        });*/
        var submission_status = 1;

        statutorysetting = [];
        var totalCompliance = 1;
       
        for(var i=1; i<=(actCount-1); i++){
            var aStatus = parseInt($('#act'+i).attr("for"));
            var remark = null;
            if($('#remark'+i).val().trim()){
                remark = $('#remark'+i).val().trim();
            }
            if((aStatus == 2 || aStatus==3) && remark==null){
                displayMessage(message.act_remarks_required);
                return false;
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
                var client_statutory_id = null;
              
                
                statutorysettingData = mirror.saveComplianceStatus(
                    int(val_group_id), int(val_legal_entity_id), 1, 
                    int(val_domain_id), comp_id, complianceStatusVal,
                    level_1_s_id, aStatus, remark, client_statutory_id
                );
                statutorysetting.push(statutorysettingData);
                totalCompliance++;
            }
        }
        console.log(statutorysetting)
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

    else if (api_type == SUBMIT_API){
        selected_compliances_list = [];
        $.each(SELECTED_COMPLIANCES, function(key, value){
            value["compliance_id"] = parseInt(key);
            selected_compliances_list.push(
                value
            );
        });
        mirror.submitAssignedStatutory(CLIENT_STATUTORY_ID, UNITS, parseInt(val_group_id), ACTIVE_UNITS, 
            selected_compliances_list, LEVEL_1_STATUTORYWISE_COMPLIANCES, 
            function(error, data) {
                if (error == null) {
                    displayMessage(message.submit_success);
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
    
   /* ActivateStep2.click(function(e) {
        if (validateFirstTab()) {
            activateWizardTwo();
            callAPI(API_Wizard2);
        }
    });*/
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
            $('.panel-title a', clone).text(value.level_1_s_name);
            $('.panel-title a', clone).attr('href', '#collapse'+actCount);
            $('.panel-title a', clone).attr('aria-controls', 'collapse'+actCount);

            $('.coll-title', clone).attr('id', 'collapse'+actCount);
            $('.coll-title', clone).attr('aria-labelledb', 'heading'+actCount);
            
            $('.change_status', clone).attr('id', 'act'+actCount);
            $('.change_status', clone).val(actCount);
            //$('.act-label', clone).attr('for', 1);
            
            $('.remarks', clone).attr('id', 'remark'+actCount);

            $('.tbody-assignstatutory').append(clone);

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
        //$('.saved', clone2).addClass('saved-icon');

        $('.comp', clone2).on('click', function () {
            compliancestatus(this);
            //setApplicabilityStatus(value.compliance_id, $(this).val(), true, 1);
        });
        
        /* if (compliance_applicable_status == false) {
            $('#statutory' + statutoriesCount).each(function () {
            this.checked = false;
            });
        }*/

        statutoriesCount++;
        count++;
        $('.remarks').on('input', function (e) {
          this.value = isCommon($(this));
        });
    
        $(' #collapse'+ccount+' .tbody-compliance-list').append(clone2);
        //$('[data-toggle="tooltip"]').tooltip();

    });
    if(sno <= 0){
        SubmitButton.hide();
        SaveButton.hide();
    }else{
        SubmitButton.show();
        SaveButton.show();
    }
}

/*function setApplicabilityStatus(
    compliance_id, applicable, not_applicable, not_at_all_applicable, saved,
    statutory_applicability_status
){
    //  1- Applicable
    //  2 - Not applicable
    //  3 - Not at all applicable
    applicablity_status = 0
    if(applicable == true){
        applicablity_status = 1;
    }else if(not_applicable == true){
        applicablity_status = 2;
    }else{
        applicablity_status = 3;
    }    
    SELECTED_COMPLIANCES[compliance_id] = {
        "compliance_applicability_status": applicablity_status,
        "is_saved": saved,
        "statutory_applicability_status": statutory_applicability_status
    }
}

function setLevel1ApplicabilityStatus(
    level_1_statutory_index, applicablity_stauts
){
    compliances = LEVEL_1_STATUTORYWISE_COMPLIANCES[level_1_statutory_index]
    $.each(compliances, function(key, value){
        var compliance_id = value;
        var applicable_class = "statu-applicable-"+level_1_statutory_index+"-"+compliance_id;
        var not_applicable_class = "statu-not-applicable-"+level_1_statutory_index+"-"+compliance_id;
        var not_at_all_applicable_class = "statu-not-at-all-applicable-"+level_1_statutory_index+"-"+compliance_id;
        var saved_class = "statu-saved-"+level_1_statutory_index+"-"+compliance_id;
        if(applicablity_stauts == 1){
            $("."+applicable_class).removeClass(ApplicableInActiveIcon);
            $("."+applicable_class).addClass(ApplicableActiveIcon);
            $("."+not_applicable_class).removeClass(NotApplicableActiveIcon);
            $("."+not_applicable_class).addClass(NotApplicableInActiveIcon);
            $("."+not_at_all_applicable_class).removeClass(NotAtAllApplicableActiveIcon);
            $("."+not_at_all_applicable_class).addClass(NotAtAllApplicableInActiveIcon);
            setApplicabilityStatus(compliance_id, true, false, false, false, 1);
        }else if(applicablity_stauts == 2){
            $("."+applicable_class).removeClass(ApplicableActiveIcon);
            $("."+applicable_class).addClass(ApplicableInActiveIcon);
            $("."+not_applicable_class).removeClass(NotApplicableInActiveIcon);
            $("."+not_applicable_class).addClass(NotApplicableActiveIcon);
            $("."+not_at_all_applicable_class).removeClass(NotAtAllApplicableActiveIcon);
            $("."+not_at_all_applicable_class).addClass(NotAtAllApplicableInActiveIcon);
            setApplicabilityStatus(compliance_id, false, true, false, false, 1);
        }else {
            $("."+applicable_class).removeClass(ApplicableActiveIcon);
            $("."+applicable_class).addClass(ApplicableInActiveIcon);
            $("."+not_applicable_class).removeClass(NotApplicableActiveIcon);
            $("."+not_applicable_class).addClass(NotApplicableInActiveIcon);
            $("."+not_at_all_applicable_class).removeClass(NotAtAllApplicableInActiveIcon);
            $("."+not_at_all_applicable_class).addClass(NotAtAllApplicableActiveIcon);
            setApplicabilityStatus(compliance_id, false, false, true, false, 1);
        }
    });
}

function changeStatusOfHeader(element, level_1_statutory_index){
    //  1- Applicable
    //  2 - Not applicable
    //  3 - Not at all applicable
    var className = $(element).attr('class').split(" ");
    if(className.indexOf(ApplicableActiveIcon) > - 1){
        $(element).removeClass(ApplicableActiveIcon);
        $(element).addClass(NotApplicableActiveIcon);
        setLevel1ApplicabilityStatus(level_1_statutory_index, 2);
    }else if(className.indexOf(NotApplicableActiveIcon) > -1){
        $(element).removeClass(NotApplicableActiveIcon);
        $(element).addClass(NotAtAllApplicableActiveIcon);
        setLevel1ApplicabilityStatus(level_1_statutory_index, 3);
    }else if(className.indexOf(NotAtAllApplicableActiveIcon) > -1){
        $(element).removeClass(NotAtAllApplicableActiveIcon);
        $(element).addClass(ApplicableActiveIcon);
        setLevel1ApplicabilityStatus(level_1_statutory_index, 1);
    }
}

function activateInactivateApplicableIcon(element_class, compliance_id){
    var element = $("."+element_class);
    var className = element.attr('class').split(" ");
    if(className.indexOf(ApplicableActiveIcon) > -1){
        element.addClass(ApplicableInActiveIcon);
        element.removeClass(ApplicableActiveIcon);
        setApplicabilityStatus(compliance_id, false, true, false, false, 1);
    }else{
        element.removeClass(ApplicableInActiveIcon);
        element.addClass(ApplicableActiveIcon);
        setApplicabilityStatus(compliance_id, true, false, false, false, 1);
    }
}

function activateInactivateNotApplicableIcon(element_class, compliance_id){
    var element = $("."+element_class);
    var className = element.attr('class').split(" ");
    if(className.indexOf(NotApplicableActiveIcon) > -1){
        element.addClass(NotApplicableInActiveIcon);
        element.removeClass(NotApplicableActiveIcon);
        setApplicabilityStatus(compliance_id, true, false, false, false, 1);
    }else{
        element.removeClass(NotApplicableInActiveIcon);
        element.addClass(NotApplicableActiveIcon);
        setApplicabilityStatus(compliance_id, false, true, false, false, 1);
    }
}

function activateInactivateNotAtAllApplicableIcon(element_class, compliance_id){
    var element = $("."+element_class);
    var className = element.attr('class').split(" ");
    if(className.indexOf(NotAtAllApplicableActiveIcon) > -1){
        element.removeClass(NotAtAllApplicableActiveIcon);
        element.addClass(NotAtAllApplicableInActiveIcon);
        setApplicabilityStatus(compliance_id, true, false, false, false, 1);
    }else{
        element.addClass(NotAtAllApplicableActiveIcon);
        element.removeClass(NotAtAllApplicableInActiveIcon);
        setApplicabilityStatus(compliance_id, false, false, true, false, 1);
    }
}*/

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
        $(TblCountry, clone).text(value.country_name);
        $(TblGroup, clone).text(value.group_name);
        $(TblBG, clone).text(value.business_group_name);
        $(TblLE, clone).text(value.legal_entity_name);
        $(TblDiv, clone).text(ifNullReturnHyphen(value.division_name));
        $(TblCat, clone).text(ifNullReturnHyphen(value.category_name));
        $(TblLoc, clone).text(value.geography_name);
        $(TblUnit, clone).text(value.unit_code_with_name);
        $(TblDomain, clone).text(value.domain_names);
        var status_text = null;
        if(value.submission_status == 0){
            status_text = "Yet to submit";
        }else if(value.submission_status == 1){
            status_text = "Pending";
        }else if(value.submission_status == 2){
            status_text = "Assigned";
        }else if(value.submission_status == 3){
            status_text = "Rejected";
        }
        $(TblStatus, clone).text(status_text);
        AssignedStatutoryList.append(clone);
        $(TblEditIcon, clone).click(function(){
            GroupName.val(value.group_name);
            BusinessGroupName.val(value.business_group_name);
            LegalEntityName.val(value.legal_entity_name);
            DivisionName.val(value.division_name);
            CategoryName.val(value.category_name);
            DomainName.val(value.domain_names);
            GroupId.val(value.client_id);
            val_group_id = value.client_id;
            BusinessGroupId.val(value.business_group_id);
            LegalEntityId.val(value.legal_entity_id);
            DivisionId.val(value.division_id);
            CategoryId.val(value.category_id);
            CLIENT_STATUTORY_ID = value.client_statutory_id;
            ACTIVE_UNITS.push(value.unit_id);
            EditAssignedStatutory()
        });
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

function EditAssignedStatutory(){
    AssignStatutoryView.hide();
    AssignStatutoryAdd.show();
    activateEditWizardTwo();
    callAPI(API_Wizard1);
    callAPI(EDIT_API);
}
function initialize() {
    pageControls();
    showList();
}

$(function() {
    initialize();
});

/*$('.statutory_mapping_tab li').click(function(e){
    alert($(e.target).parent().attr('class').hasClass("disabled"))
});*/