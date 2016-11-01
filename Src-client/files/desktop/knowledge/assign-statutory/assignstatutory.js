/* Elements */
var AddButton = $(".btn-assignstatutory-add");
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

var Show = $(".btn-show");
var SelectedUnitCount = $(".selected_checkbox_count");
var ChangeAccordianHeaderStatus = ".change_status";

var ActivateStep2 = $("#activate-step-2");
var Step1Header = $(".step1header");
var Step2Header = $(".step2header");
var Step1 = $("#step-1");
var Step2 = $("#step-2");
var BreadCrumbs = $(".breadcrumbs");
var BreadCrumbImg = $(".bread-crum-img img");

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

var Submit = $("#assign-statutory-submit");
var Save = $("#assign-statutory-save");
var Previous = $("#previous");

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
                GROUPS = data.clients;
                BUSINESS_GROUPS = data.business_groups;
                LEGAL_ENTITIES = data.unit_legal_entity;
                DIVISIONS = data.divisions;
                CATEGORIES = data.categories;
                UNITS = data.unit_id_name;
                DOMAINS = data.domains;
            } else {
                custom_alert(error);
            }
        });
    }

    else if (api_type == API_Wizard2) {
        mirror.getAssignStatutoryWizardTwoData(
            int(val_group_id), int(val_business_group_id), int(val_legal_entity_id),
            int(val_division_id), int(val_category_id), int(val_domain_id), ACTIVE_UNITS,
            function(error, data) {
                if (error == null) {
                    LEVEL_1_STATUTORIES = data.level_1_statutories_list;
                    COMPLIANCES_LIST = data.statutories_for_assigning;
                    loadCompliances();
                } else {
                    custom_alert(error);
                }
            }
        );
    }

    else if (api_type == SAVE_API){
        selected_compliances_list = [];
        $.each(SELECTED_COMPLIANCES, function(key, value){
            value["compliance_id"] = parseInt(key);
            selected_compliances_list.push(
                value
            );
        });
        mirror.saveAssignedStatutory(CLIENT_STATUTORY_ID, UNITS, parseInt(val_group_id), ACTIVE_UNITS,
            selected_compliances_list, LEVEL_1_STATUTORYWISE_COMPLIANCES,
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
    AddButton.click(function() {
        AssignStatutoryView.hide();
        AssignStatutoryAdd.show();
        callAPI(API_Wizard1);
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

    Submit.click(function(){
        callAPI(SUBMIT_API);
    });
    
    Save.click(function(){
        callAPI(SAVE_API);
    });

    Previous.click(function(){
        Step1Header.addClass('active');
        Step1Header.removeClass('inactive');
        Step2Header.addClass('disabled');
        Step2Header.removeClass('active');
        Step1.show();
        Step2.hide();
    });

    ActivateStep2.click(function(e) {
        if (validateFirstTab()) {
            activateWizardTwo();
            callAPI(API_Wizard2);
        }
    });

    Step1Header.click(function(e) {
        Step1Header.addClass('active');
        Step1Header.removeClass('inactive');
        Step2Header.addClass('disabled');
        Step2Header.removeClass('active');
        Step1.show();
        Step2.hide();
    });
}

function activateWizardTwo(){
    clearMessage();
    Step2Header.addClass('active');
    Step2Header.removeClass('disabled');
    Step1Header.addClass('inactive');
    Step1Header.removeClass('active');
    Step1.hide();
    Step2.show();
    showBreadCrumbText();
}

function activateEditWizardTwo(){
    clearMessage();
    Step2Header.addClass('active');
    Step2Header.removeClass('disabled');
    Step1Header.addClass('disabled');
    Step1Header.removeClass('active');
    Step1.hide();
    Step2.show();
    Previous.hide();
    showBreadCrumbText();
}

function showBreadCrumbText() {
    BreadCrumbs.empty();
    var img_clone = BreadCrumbImg.clone();
    BreadCrumbs.append(GroupName.val() + " ");

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
    val_business_group_id = BusinessGroupId.val();
    val_legal_entity_id = LegalEntityId.val();
    val_division_id = DivisionId.val();
    val_category_id = CategoryId.val();
    val_domain_id = DomainId.val();
    if (val_group_id.trim().length <= 0) {
        displayMessage(message.group_required);
        return false;
    } else if (val_legal_entity_id.trim().length <= 0) {
        displayMessage(message.legalentity_required);
        return false;
    } else {
        loadUnits();
    }
}

function loadUnits() {
    UnitList.empty();
    $.each(UNITS, function(key, value) {
        var validation_result = true;
        if (val_business_group_id) {
            if (val_business_group_id == value.business_group_id) {
                validation_result = true;
            } else {
                validation_result = false;
            }
        }
        if (val_division_id) {
            if (val_division_id == value.division_id) {
                validation_result = validation_result & true;
            } else {
                validation_result = validation_result & false;
            }
        }
        if (val_category_id) {
            if (val_category_id == value.category_id) {
                validation_result = validation_result & true;
            } else {
                validation_result = validation_result & false;
            }
        }
        if (val_domain_id) {
            if (val_domain_id == value.domain_id) {
                validation_result = validation_result & true;
            } else {
                validation_result = validation_result & false;
            }
        }
        if (validation_result == null) {
            validation_result = true;
        }
        if (
            value.client_id == val_group_id &&
            value.legal_entity_id == val_legal_entity_id &&
            validation_result
        ) {
            unit_text = value.unit_code + " - " + value.unit_name + " - " + value.address;
            var clone = UnitRow.clone();
            clone.text(unit_text);
            UnitList.append(clone);
            clone.click(function() {
                activateUnit(this, value.unit_id);
            });
        }
    });
}

function activateUnit(element, unit_id) {
    var chkstatus = $(element).attr('class');
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        index = ACTIVE_UNITS.indexOf(unit_id)
        ACTIVE_UNITS.splice(index, 1);
    } else {
        $(element).addClass('active');
        ACTIVE_UNITS.push(unit_id);
    }
    SelectedUnitCount.text(ACTIVE_UNITS.length);
}

function validateFirstTab() {
    if (ACTIVE_UNITS.length <= 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
        return true;
    }
}

function loadCompliances() {
    AssignStatutoryList.empty();
    $.each(LEVEL_1_STATUTORIES, function(key, value) {
        var clone = AccordianHeader.clone();
        $(ACT_NAME, clone).text(value);
        $(StatutoryValuesList, clone).addClass("statu-" + key);
        AssignStatutoryList.append(clone);
        $(ChangeAccordianHeaderStatus, clone).click(function(){
            changeStatusOfHeader(this, key);
        });
    });

    var sno = 0;
    $.each(COMPLIANCES_LIST, function(key, value) {
        ++sno;
        list_class = $(".statu-" + value.level_1_statutory_index);
        if (list_class.find("tr").length <= 1) {
            var headerclone = StatutoryHeader.clone();
            list_class.append(headerclone);
        }
        var value_clone = StatutoryValue.clone();
        $(SNo, value_clone).text(sno);
        $(StatutoryProvision, value_clone).text(value.statutory_provision);
        $(ComplianceTask, value_clone).text(value.compliance_name);
        $(ComplianceDescription, value_clone).text(value.description);

        var applicable_class = "statu-applicable-"+value.level_1_statutory_index+"-"+value.compliance_id;
        var not_applicable_class = "statu-not-applicable-"+value.level_1_statutory_index+"-"+value.compliance_id;
        var not_at_all_applicable_class = "statu-not-at-all-applicable-"+value.level_1_statutory_index+"-"+value.compliance_id;
        var saved_class = "statu-saved-"+value.level_1_statutory_index+"-"+value.compliance_id;

        $(Applicable, value_clone).addClass(ApplicableActiveIcon);
        $(Applicable, value_clone).addClass(applicable_class);

        $(NotApplicable, value_clone).addClass(NotApplicableInActiveIcon);
        $(NotApplicable, value_clone).addClass(not_applicable_class);

        $(NotAtAllApplicable, value_clone).addClass(NotAtAllApplicableInActiveIcon);
        $(NotAtAllApplicable, value_clone).addClass(not_at_all_applicable_class);

        $(IsSaved, value_clone).addClass(SavedInActiveIcon);
        $(IsSaved, value_clone).addClass(saved_class);

        list_class.append(value_clone);
        $("."+applicable_class).click(function(e){
            activateInactivateApplicableIcon(
                applicable_class, value.compliance_id);
        });
        $("."+not_applicable_class).click(function(){
            activateInactivateNotApplicableIcon(
                not_applicable_class, value.compliance_id);
        });
        $("."+not_at_all_applicable_class).click(function(){
            activateInactivateNotAtAllApplicableIcon(
                not_at_all_applicable_class, value.compliance_id);
        });
        setApplicabilityStatus(value.compliance_id, true, false, false, false, 1);
        if(!(value.level_1_statutory_index in LEVEL_1_STATUTORYWISE_COMPLIANCES)){
            LEVEL_1_STATUTORYWISE_COMPLIANCES[value.level_1_statutory_index] = [];
        }
        LEVEL_1_STATUTORYWISE_COMPLIANCES[value.level_1_statutory_index].push(
            value.compliance_id);
    });
    if(sno <= 0){
        Save.hide();
        Submit.hide();
    }else{
        Save.show();
        Submit.show();
    }
}

function setApplicabilityStatus(
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
}

function showList(){
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

