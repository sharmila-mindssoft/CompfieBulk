/* Elements */
var CURRENT_TAB = 1;
var AddButton = $(".btn-assignstatutory-add");
var CancelButton = $('#btn-user-cancel');
var AssignStatutoryView = $("#assignstatutory-view");
var AssignStatutoryAdd = $("#assignstatutory-add");
var Show = $(".btn-show");
var ShowMore = $(".btn-showmore");

var NextButton = $('#btn-next');
var PreviousButton = $('#btn-previous');
var SubmitButton = $("#btn-submit");
var SaveButton = $("#btn-save");
var UnitSearch = $('#unit-search');

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
var SingleAssignStatutoryList = $(".tbody-single-assignstatutory");
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
var UNIT_CS_ID = {};
var bred_crump_text = null;
var CLIENT_STATUTORY_ID = null;
var UNIT_TEXT = null;
var DOMAIN_TEXT = null;

/* API Types */
var API_Wizard1 = "wizard_1";
var API_Wizard2 = "wizard_2";
var SAVE_API = "save";
var SUBMIT_API = "submit";
var API_LIST = "list";
var EDIT_API = "edit"

var LastAct = '';
var LastSubAct = '';
var LastCompliance = '';
var statutoriesCount = 1;
var actCount = 1;
var count = 1;
var sno = 1;
var totalRecord = 0;
AssignStatutoryList.empty();
SingleAssignStatutoryList.empty();
var SELECTED_COMPLIANCE = {};
var ACT_MAP = {};


function callAPI(api_type) {
    if (api_type == API_LIST) {
        displayLoader();
        mirror.getAssignedStatutories(function(error, data) {
            if (error == null) {
                ASSIGNED_STATUTORIES = data.assigned_statutories;
                loadAssignedStatutories();

            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == API_Wizard1) {
        displayLoader();
        mirror.getAssignStatutoryWizardOneData(function(error, data) {
            if (error == null) {
                GroupName.focus();
                GROUPS = data.grps;
                BUSINESS_GROUPS = data.bgrps;
                LEGAL_ENTITIES = data.lety;
                DIVISIONS = data.divs;
                CATEGORIES = data.cates;
                DOMAINS = data.dms;
                hideLoader();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == API_Wizard2) {
        COMPLIANCES_LIST = [];
        displayLoader();
        var r_count = 0;
        if (ACTIVE_UNITS.length == 1) {
            r_count = sno - 1;
        } else {
            r_count = statutoriesCount - 1;
        }

        mirror.getAssignStatutoryWizardTwoData(
            int(val_domain_id), ACTIVE_UNITS, r_count,
            function(error, data) {
                if (error == null) {
                    if (ACTIVE_UNITS.length == 1) {
                        COMPLIANCES_LIST = data.statutories_for_assigning;
                        loadSingleUnitCompliances();
                    } else {
                        COMPLIANCES_LIST = data.statutories_for_multiple;
                        loadMultipleUnitCompliances();
                    }
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            }
        );
    } else if (api_type == SAVE_API || api_type == SUBMIT_API) {

        //check request is save or submit
        var submission_status;
        if (api_type == SAVE_API) {
            submission_status = 1;
        } else {
            submission_status = 2;
        }

        //check all compliance is selected before submit
        var checkSubmit = false;
        if($('.comp:checked').length == (statutoriesCount - 1)){
            checkSubmit = true;
        }

        //check remark validation
        for(var i=1; i<=(actCount-1); i++){
            var aStatus = parseInt($('#act'+i).attr("for"));
            var remark = null;
            if(aStatus == 2 || aStatus==3){
                remark = $('#remark'+i).val().trim();
                if(remark==''){
                    displayMessage(message.remarks_required);
                    hideLoader();
                    return false;
                }else if (validateMaxLength("remark", remark, "Remark") == false) {
                    hideLoader();
                    return false;
                }
            }
        }

        var selected_compliances_list = [];
        $.each(SELECTED_COMPLIANCE, function(key, value) {
            selected_compliances_list.push(
                value
            );
        });

        if (submission_status == 1 && selected_compliances_list.length == 0) {
            displayMessage(message.no_updation_in_assign_statu);
            hideLoader();
            return false;
        }
        else if (submission_status == 2 && checkSubmit == false) {
            displayMessage(message.assigncompliance_submit_failure);
            hideLoader();
            return false;
        } else {
            bgName = null;
            if(BusinessGroupName.val() != ''){
                bgName = BusinessGroupName.val();
            }
            mirror.saveAssignedStatutory(selected_compliances_list, submission_status, int(val_group_id), int(val_legal_entity_id),
                int(val_domain_id), DomainName.val(), ACTIVE_UNITS, LegalEntityName.val(), bgName,
                function(error, data) {
                    if (error == null) {

                        if(submission_status == 2){
                            displaySuccessMessage(message.assign_statutory_submit_success);
                        }else if (CLIENT_STATUTORY_ID != null) {
                            displaySuccessMessage(message.assign_statutory_updated_success);
                        } else {
                            displaySuccessMessage(message.assign_statutory_save_success);
                        }

                        CLIENT_STATUTORY_ID = null;
                        showList();
                        hideLoader();
                    } else {
                        displayMessage(error);
                        hideLoader();
                    }
                }
            );
        }

    }

}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'group_id') {
        BusinessGroupName.val('');
        BusinessGroupId.val('');
        LegalEntityName.val('');
        LegalEntityId.val('');
        DivisionName.val('');
        DivisionId.val('');
        CategoryName.val('');
        CategoryId.val('');
        DomainName.val('');
        DomainId.val('');
    } else if (current_id == 'business_group_id') {
        LegalEntityName.val('');
        LegalEntityId.val('');
        DivisionName.val('');
        DivisionId.val('');
        CategoryName.val('');
        CategoryId.val('');
        DomainName.val('');
        DomainId.val('');
    } else if (current_id == 'legal_entity_id') {
        DivisionName.val('');
        DivisionId.val('');
        CategoryName.val('');
        CategoryId.val('');
        DomainName.val('');
        DomainId.val('');
    } else if (current_id == 'division_id') {
        CategoryName.val('');
        CategoryId.val('');
    }
    UnitList.empty();
    ACTIVE_UNITS = [];
}

function pageControls() {

    NextButton.click(function() {
        $('.tbody-compliance-list').empty();
        CURRENT_TAB += 1;
        showTab();
    });
    PreviousButton.click(function() {
        $(".total_count_view").hide();
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
    });

    AddButton.click(function() {
        reset();
        showTab();
        $(".total_count_view").hide();
        AssignStatutoryView.hide();
        AssignStatutoryAdd.show();
        callAPI(API_Wizard1);
    });

    ShowMore.click(function() {
        callAPI(API_Wizard2);
    });

    CancelButton.click(function() {
        CURRENT_TAB = 1;
        AssignStatutoryView.show();
        AssignStatutoryAdd.hide();
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

        if (GroupId.val() != '') {
            var condition_fields = ["client_id"];
            var condition_values = [GroupId.val()];

            var text_val = $(this).val();
            commonAutoComplete(
                e, ACBusinessGroup, BusinessGroupId, text_val,
                BUSINESS_GROUPS, "business_group_name", "business_group_id",
                function(val) {
                    onAutoCompleteSuccess(BusinessGroupName, BusinessGroupId, val);
                }, condition_fields, condition_values);
        }
    });

    LegalEntityName.keyup(function(e) {
        if (GroupId.val() != '') {
            var condition_fields = ["client_id"];
            var condition_values = [GroupId.val()];
            if (BusinessGroupId.val() != '') {
                condition_fields.push("business_group_id");
                condition_values.push(BusinessGroupId.val());
            }
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACLegalEntity, LegalEntityId, text_val,
                LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
                function(val) {
                    onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
                }, condition_fields, condition_values);
        }
    });

    DivisionName.keyup(function(e) {
        if (GroupId.val() != '') {
            var condition_fields = ["client_id", "legal_entity_id"];
            var condition_values = [GroupId.val(), LegalEntityId.val()];
            if (BusinessGroupId.val() != '') {
                condition_fields.push("business_group_id");
                condition_values.push(BusinessGroupId.val());
            }
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACDivision, DivisionId, text_val,
                DIVISIONS, "division_name", "division_id",
                function(val) {
                    onAutoCompleteSuccess(DivisionName, DivisionId, val);
                }, condition_fields, condition_values);
        }
    });

    CategoryName.keyup(function(e) {
        if (GroupId.val() != '') {
            var condition_fields = ["client_id", "legal_entity_id"];
            var condition_values = [GroupId.val(), LegalEntityId.val()];
            if (BusinessGroupId.val() != '') {
                condition_fields.push("business_group_id");
                condition_values.push(BusinessGroupId.val());
            }
            if (DivisionId.val() != '') {
                condition_fields.push("division_id");
                condition_values.push(DivisionId.val());
            }
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACCategory, CategoryId, text_val,
                CATEGORIES, "category_name", "category_id",
                function(val) {
                    onAutoCompleteSuccess(CategoryName, CategoryId, val);
                }, condition_fields, condition_values);
        }
    });

    DomainName.keyup(function(e) {
        if (LegalEntityId.val() != '') {
            var condition_fields = ["legal_entity_id"];
            var condition_values = [LegalEntityId.val()];

            var text_val = $(this).val();
            commonAutoComplete(
                e, ACDomain, DomainId, text_val,
                DOMAINS, "domain_name", "domain_id",
                function(val) {
                    onAutoCompleteSuccess(DomainName, DomainId, val);
                }, condition_fields, condition_values);
        }
    });
    Show.click(function() {
        validateAndShow();
    });

    SubmitButton.click(function() {
        displayLoader();
        setTimeout(function() {
            callAPI(SUBMIT_API)
        }, 500);
    });

    SaveButton.click(function() {
        displayLoader();
        setTimeout(function() {
            callAPI(SAVE_API)
        }, 500);
    });

    SelectAll.click(function() {
        ACTIVE_UNITS = [];
        //UNIT_CS_ID = {};
        if (UNITS != null && UNITS.length > 0) {
            $('.unit-list li').each(function(index, el) {
                if (ACTIVE_UNITS.length >= 20) {
                    displayMessage(message.maximum_units);
                    return false;
                } else {
                    if (SelectAll.prop('checked')) {
                        $(el).addClass('active');
                        $(el).find('i').addClass('fa fa-check pull-right');
                        var chkid = $(el).attr('id');
                        ACTIVE_UNITS.push(parseInt(chkid));
                    } else {
                        $(el).removeClass('active');
                        $(el).find('i').removeClass('fa fa-check pull-right');
                    }
                }
            });
            SelectedUnitCount.text(ACTIVE_UNITS.length);
        }

    });

    UnitSearch.keyup(function() {
        var searchText = $(this).val().toLowerCase();
        $('.unit-list > li').each(function() {
            var currentLiText = $(this).text().toLowerCase();
            showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });
}

function reset() {
    GroupId.val('');
    GroupName.val('');
    BusinessGroupName.val('');
    LegalEntityName.val('');
    DivisionName.val('');
    CategoryName.val('');
    DomainName.val('');
    val_group_id = null;
    val_domain_id = null;
    val_legal_entity_id = null;
    CLIENT_STATUTORY_ID = null;
    UNIT_TEXT = null;
    DOMAIN_TEXT = null;
    AssignStatutoryList.empty();
    SingleAssignStatutoryList.empty();
    UnitList.empty();
    ACTIVE_UNITS = [];
    SELECTED_COMPLIANCE = {};
    ACT_MAP = {};
    SelectAll.prop("checked", false);
    SelectedUnitCount.text(ACTIVE_UNITS.length);
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
        displayLoader();
        mirror.getAssignStatutoryWizardOneDataUnits(int(val_group_id), int(val_business_group_id),
            int(val_legal_entity_id), int(val_division_id), int(val_category_id), int(val_domain_id),
            function(error, data) {
                if (error == null) {
                    UNITS = data.statu_units;
                    loadUnits();
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            });
    }
}

function loadUnits() {
    ACTIVE_UNITS = [];
    SelectAll.prop("checked", false);
    SelectedUnitCount.text(ACTIVE_UNITS.length);
    UnitList.empty();
    UNIT_CS_ID = {};
    if (UNITS.length == 0) {
        var clone = UnitRow.clone();
        clone.text('No Units Found');
        UnitList.append(clone);
    } else {
        $.each(UNITS, function(key, value) {
            unit_idval = value.u_id;
            unit_text = value.unit_code + " - " + value.u_name + " - " + value.address;
            var clone = UnitRow.clone();
            clone.html(unit_text + '<i></i>');
            clone.attr('id', unit_idval);
            UnitList.append(clone);
            clone.click(function() {
                activateUnit(this);
            });
            UNIT_CS_ID[value.u_id] = value;
        });
    }
}

function activateUnit(element) {

    var chkstatus = $(element).attr('class');
    var chkid = $(element).attr('id');
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
        index = ACTIVE_UNITS.indexOf(parseInt(chkid));
        ACTIVE_UNITS.splice(index, 1);
    } else {
        if (ACTIVE_UNITS.length >= 20) {
            displayMessage(message.maximum_units);
            return false;
        }else{
            $(element).addClass('active');
            $(element).find('i').addClass('fa fa-check pull-right');
            ACTIVE_UNITS.push(parseInt(chkid));
        }
    }
    SelectedUnitCount.text(ACTIVE_UNITS.length);
}

function actstatus(element, A_ID) {
    var checkedVal = parseInt($(element).attr("for"));
    var remarkbox = '#r-view' + $(element).val();
    var A_REMARK = null;

    if (checkedVal > 1) {
        $(remarkbox).show();
        $('#remark' + $(element).val()).val('');
        /*if($('#remark' + $(element).val()).val() != ''){
            A_REMARK = $('#remark' + $(element).val()).val();
        }*/
    } else {
        $(remarkbox).hide();
    }

    var currentAction = '';
    if (checkedVal == 1) {
        currentAction = '.tick' + $(element).val();
    } else if (checkedVal == 2) {
        currentAction = '.untick' + $(element).val();
    } else {
        currentAction = '.minus' + $(element).val();
    }

    $(currentAction).each(function() {
        var C_S_ID = null;
        $(this).prop("checked", true);
        var sname = $(this).attr('name');
        var sid = sname.substr(sname.lastIndexOf('y') + 1);
        $('#save' + sid).addClass('fa-square');

        var combine_ids = $('#combineid' + sid).val().split('#');
        if (CLIENT_STATUTORY_ID == null) {
            C_S_ID = UNIT_CS_ID[combine_ids[1]].client_statutory_id;
            UNIT_TEXT = UNIT_CS_ID[combine_ids[1]].unit_code + ' - ' + UNIT_CS_ID[combine_ids[1]].u_name;
        }else{
            C_S_ID = CLIENT_STATUTORY_ID;
        }

        SELECTED_COMPLIANCE[combine_ids[0]] = {
            'u_id': parseInt(combine_ids[1]),
            'comp_id': parseInt(combine_ids[0]),
            'comp_status': checkedVal,
            'level_1_s_id': A_ID,
            'a_status': checkedVal,
            'remarks': A_REMARK,
            'client_statutory_id': C_S_ID,
            'u_name': UNIT_TEXT
        }
        //console.log(SELECTED_COMPLIANCE)
    });
}

function remarkstatus(element, A_ID) {
    var ID = $(element).attr("data-act");
    var A_STATUS = parseInt($('#act' + ID).attr("for"));
    var A_REMARK = null;
    if($(element).val() != ''){
        A_REMARK = $(element).val();
    }

    var currentAction = '.tick' + ID;
    $(currentAction).each(function() {
        var C_S_ID = null;
        var sname = $(this).attr('name');
        var sid = sname.substr(sname.lastIndexOf('y') + 1);
        var combine_ids = $('#combineid' + sid).val().split('#');
        if (CLIENT_STATUTORY_ID == null) {
            C_S_ID = UNIT_CS_ID[combine_ids[1]].client_statutory_id;
            UNIT_TEXT = UNIT_CS_ID[combine_ids[1]].unit_code + ' - ' + UNIT_CS_ID[combine_ids[1]].u_name;
        }else{
            C_S_ID = CLIENT_STATUTORY_ID;
        }

        var C_STATUS = null;
        if($('input[name=statutory'+sid+']:checked').val() != undefined){
            C_STATUS = parseInt($('input[name=statutory'+sid+']:checked').val());
        }

        if (C_STATUS > 1) {
            SELECTED_COMPLIANCE[combine_ids[0]] = {
                'u_id': parseInt(combine_ids[1]),
                'comp_id': parseInt(combine_ids[0]),
                'comp_status': C_STATUS,
                'level_1_s_id': A_ID,
                'a_status': A_STATUS,
                'remarks': A_REMARK,
                'client_statutory_id': C_S_ID,
                'u_name': UNIT_TEXT
            }
        }
    });
    //console.log(SELECTED_COMPLIANCE);
}

function compliancestatus(element, C_ID, U_ID, A_ID) {
    var C_S_ID = null;
    var sname = $(element).attr('name');
    var sid = sname.substr(sname.lastIndexOf('y') + 1);
    $('#save' + sid).addClass('fa-square');

    var combine_ids = $('#combineid' + sid).val().split('#');
    /*var l_calss = $(element).attr('class').split(' ').pop();
    var id = l_calss.substr(l_calss.lastIndexOf('s') + 1);
    alert($('#act' + id).attr("for"))*/
    var A_STATUS = $('#act' + combine_ids[2]).attr("for");
    var A_REMARK = null;

    var C_STATUS = parseInt($(element).val());
    if (C_STATUS > 1 && $('#remark' + combine_ids[2]).val() != '') {
        A_REMARK = $('#remark' + combine_ids[2]).val();
    }
    if (CLIENT_STATUTORY_ID == null) {
        C_S_ID = UNIT_CS_ID[U_ID].client_statutory_id;
        UNIT_TEXT = UNIT_CS_ID[U_ID].unit_code + ' - ' + UNIT_CS_ID[U_ID].u_name;
    }else{
        C_S_ID = CLIENT_STATUTORY_ID;
    }

    SELECTED_COMPLIANCE[C_ID] = {
        'u_id': parseInt(U_ID),
        'comp_id': parseInt(C_ID),
        'comp_status': C_STATUS,
        'level_1_s_id': parseInt(A_ID),
        'a_status': parseInt(A_STATUS),
        'remarks': A_REMARK,
        'client_statutory_id': C_S_ID,
        'u_name': UNIT_TEXT
    }
    //console.log(SELECTED_COMPLIANCE);
}

function mactstatus(element) {
    $('.sub-comp').prop("checked", false);
    var A_ID = parseInt($(element).attr("data-act-id"));
    var ID = $(element).attr("data-act");

    var checkedVal = parseInt($(element).attr("for"));

    var remarkbox = '#r-view' + ID;
    var A_REMARK = null;

    if (checkedVal > 1) {
        $(remarkbox).show();
        $('#remark' + ID).val('');
        /*if($('#remark' + ID).val() != ''){
            A_REMARK = $('#remark' + ID).val();
        }*/
    } else {
        $(remarkbox).hide();
    }

    var currentAction = '';
    if (checkedVal == 1) {
        currentAction = '.tick' + ID;
    } else if (checkedVal == 2) {
        currentAction = '.untick' + ID;
    } else {
        currentAction = '.minus' + ID;
    }

    $(currentAction).each(function() {
        //alert($(this).attr('name'))
        var C_S_ID = null;
        $(this).prop("checked", true);
        var sname = $(this).attr('name');
        var sid = sname.substr(sname.lastIndexOf('y') + 1);
        $('#save' + sid).addClass('fa-square');

        var combine_ids = $('#combineid' + sid).val().split('#');
        if (CLIENT_STATUTORY_ID == null) {
            C_S_ID = UNIT_CS_ID[combine_ids[1]].client_statutory_id;
            UNIT_TEXT = UNIT_CS_ID[combine_ids[1]].unit_code + ' - ' + UNIT_CS_ID[combine_ids[1]].u_name;
        }else{
            C_S_ID = CLIENT_STATUTORY_ID;
        }
        var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
        SELECTED_COMPLIANCE[C_U_ID] = {
            'u_id': parseInt(combine_ids[1]),
            'comp_id': parseInt(combine_ids[0]),
            'comp_status': checkedVal,
            'level_1_s_id': A_ID,
            'a_status': checkedVal,
            'remarks': A_REMARK,
            'client_statutory_id': C_S_ID,
            'u_name': UNIT_TEXT
        }
    });
    //console.log(SELECTED_COMPLIANCE)
}

function mcompliancestatus(element) {
    var C_S_ID = null;
/*  var sname = $(element).attr('class');
    var sid = sname.substr(sname.lastIndexOf('-') + 1);*/

    var sname1 = $(element).attr('name');
    var sid1 = sname1.substr(sname1.lastIndexOf('y') + 1);
    $('#save' + sid1).addClass('fa-square');
    var combine_ids = $('#combineid' + sid1).val().split('#');
    var C_ID = combine_ids[0];
    var U_ID = combine_ids[1];
    var A_ID = combine_ids[2];
    var ID = combine_ids[3];

    var A_STATUS = $('#act' + ID).attr("for");
    var A_REMARK = null;
    var C_STATUS = parseInt($(element).val());
    if (C_STATUS > 1 && $('#remark' + ID).val() != '') {
        A_REMARK = $('#remark' + ID).val();
    }
    if (CLIENT_STATUTORY_ID == null) {
        C_S_ID = UNIT_CS_ID[U_ID].client_statutory_id;
        UNIT_TEXT = UNIT_CS_ID[U_ID].unit_code + ' - ' + UNIT_CS_ID[U_ID].u_name;
    }else{
        C_S_ID = CLIENT_STATUTORY_ID;
    }

    var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
    SELECTED_COMPLIANCE[C_U_ID] = {
        'u_id': parseInt(U_ID),
        'comp_id': parseInt(C_ID),
        'comp_status': C_STATUS,
        'level_1_s_id': parseInt(A_ID),
        'a_status': parseInt(A_STATUS),
        'remarks': A_REMARK,
        'client_statutory_id': C_S_ID,
        'u_name': UNIT_TEXT
    }
    //console.log(SELECTED_COMPLIANCE);
}


function mremarkstatus(element) {
    var ID = $(element).attr("data-act");
    var A_STATUS = parseInt($('#act' + ID).attr("for"));
    var A_REMARK = null;
    if($(element).val() != ''){
        A_REMARK = $(element).val();
    }

    var currentAction = '.tick' + ID;
    $(currentAction).each(function() {
        var C_S_ID = null;
        var sname = $(this).attr('name');
        var sid = sname.substr(sname.lastIndexOf('y') + 1);
        var combine_ids = $('#combineid' + sid).val().split('#');
        if (CLIENT_STATUTORY_ID == null) {
            C_S_ID = UNIT_CS_ID[combine_ids[1]].client_statutory_id;
            UNIT_TEXT = UNIT_CS_ID[combine_ids[1]].unit_code + ' - ' + UNIT_CS_ID[combine_ids[1]].u_name;
        }else{
            C_S_ID = CLIENT_STATUTORY_ID;
        }

        var C_STATUS = null;
        if($('input[name=statutory'+sid+']:checked').val() != undefined){
            C_STATUS = parseInt($('input[name=statutory'+sid+']:checked').val());
        }

        if (C_STATUS > 1) {
            var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
            SELECTED_COMPLIANCE[C_U_ID] = {
                'u_id': parseInt(combine_ids[1]),
                'comp_id': parseInt(combine_ids[0]),
                'comp_status': C_STATUS,
                'level_1_s_id': parseInt(combine_ids[2]),
                'a_status': A_STATUS,
                'remarks': A_REMARK,
                'client_statutory_id': C_S_ID,
                'u_name': UNIT_TEXT
            }
        }
    });
    //console.log(SELECTED_COMPLIANCE);
}

function subComplianceStatus(element) {
    var id = $(element).attr('id');
    var sid = id.substr(id.lastIndexOf('-') + 1);
    
    $('#sub-tick-'+sid).prop("checked", false);
    $('#sub-untick-'+sid).prop("checked", false);
    $('#sub-minus-'+sid).prop("checked", false);
    $(element).prop("checked", true);

    if ($(element).is(':checked')) {
        $('.' + id).each(function() {
            var C_S_ID = null;
            $(this).prop("checked", true);
            var C_STATUS = parseInt($(this).val());

            var sname = $(this).attr('name');
            var sid = sname.substr(sname.lastIndexOf('y') + 1);
            $('#save' + sid).addClass('fa-square');
            var combine_ids = $('#combineid' + sid).val().split('#');

            var ID = combine_ids[3];

            var A_STATUS = parseInt($('#act' + ID).attr("for"));
            var A_REMARK = null;
            if (C_STATUS > 1 && $('#remark' + ID).val() != '') {
                A_REMARK = $('#remark' + ID).val();
            }

            if (CLIENT_STATUTORY_ID == null) {
                C_S_ID = UNIT_CS_ID[combine_ids[1]].client_statutory_id;
                UNIT_TEXT = UNIT_CS_ID[combine_ids[1]].unit_code + ' - ' + UNIT_CS_ID[combine_ids[1]].u_name;
            }else{
                C_S_ID = CLIENT_STATUTORY_ID;
            }
            var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
            SELECTED_COMPLIANCE[C_U_ID] = {
                'u_id': parseInt(combine_ids[1]),
                'comp_id': parseInt(combine_ids[0]),
                'comp_status': C_STATUS,
                'level_1_s_id': parseInt(combine_ids[2]),
                'a_status': A_STATUS,
                'remarks': A_REMARK,
                'client_statutory_id': C_S_ID,
                'u_name': UNIT_TEXT
            }
        });
        //console.log(SELECTED_COMPLIANCE);
    }

    /*var flag = true;
    $('#save' + sid).addClass('fa-square');
    if (!$(element).is(':checked')) {
        flag = false;
        $('#save' + sid).removeClass('fa-square');
    } else {
        $('#save' + sid).addClass('fa-square');
    }
    $('.' + id).each(function() {
        $(this).prop("checked", flag);
    });*/
}

function loadSingleUnitCompliances() {

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

            $('.change_status', clone).attr('id', 'act' + actCount);
            $('.change_status', clone).val(actCount);


            $('.r-view', clone).attr('id', 'r-view' + actCount);
            $('.remarks', clone).attr('id', 'remark' + actCount);
            $('.remarks', clone).attr("data-act", actCount);

            $('.tbody-single-assignstatutory').append(clone);

            if (value.a_status == 2) {
                $('#act' + actCount).html('<img src="images/deletebold.png">').attr('for', '2');
                $('#remark' + actCount).val(value.remarks);
                $('#r-view' + actCount).show();
            } else if (value.a_status == 3) {
                $('#act' + actCount).html('<img src="images/iconminusactive.png">').attr('for', '3');
                $('#remark' + actCount).val(value.remarks);
                $('#r-view' + actCount).show();
            } else {
                $('#act' + actCount).html('<img src="images/tick1bold.png">').attr('for', '1');
            }

            $('#act' + actCount).click(function() {
                if ($(this).attr('for') == "1") {
                    $(this).html('<img src="images/deletebold.png">').attr('for', '2');
                } else if ($(this).attr('for') == "2") {
                    $(this).html('<img src="images/iconminusactive.png">').attr('for', '3');
                } else {
                    $(this).html('<img src="images/tick1bold.png">').attr('for', '1');
                }
                actstatus(this, value.level_1_s_id);
            });

            $('#remark' + actCount).focusout(function() {
                remarkstatus(this, value.level_1_s_id);
            });

            $('.remarks').on('input', function(e) {
                this.value = isCommon($(this));
            });

            count = actCount;
            LastAct = value.level_1_s_name;
            LastSubAct = "";
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
        var combineId = value.comp_id + '#' + value.u_id + '#' + count;
        $('.combineid-class', clone2).attr('id', 'combineid' + statutoriesCount);
        $('.combineid-class', clone2).val(combineId);

        if (value.s_s == 0) {
            clone2.addClass('new_row');
        } else if (value.s_s == 4) {
            clone2.addClass('rejected_row');
        }

        $('.sno', clone2).text(statutoriesCount);
        $('.statutoryprovision', clone2).text(value.s_provision);
        $('.compliancetask', clone2).text(value.comp_name);
        $('.org-name', clone2).attr('title', 'Organizations: ' + value.org_names);
        $('.compliancedescription', clone2).text(value.descrip);

        $('.compliance-ck-box-1', clone2).attr('name', 'statutory' + statutoriesCount);
        $('.compliance-ck-box-1', clone2).attr('id', 'tick' + statutoriesCount);
        $('.compliance-ck-box-1', clone2).addClass('tick' + count);
        $('.compliance-label-1', clone2).attr('for', 'tick' + statutoriesCount);

        $('.compliance-ck-box-2', clone2).attr('name', 'statutory' + statutoriesCount);
        $('.compliance-ck-box-2', clone2).attr('id', 'untick' + statutoriesCount);
        $('.compliance-ck-box-2', clone2).addClass('untick' + count);
        $('.compliance-label-2', clone2).attr('for', 'untick' + statutoriesCount);

        $('.compliance-ck-box-3', clone2).attr('name', 'statutory' + statutoriesCount);
        $('.compliance-ck-box-3', clone2).attr('id', 'minus' + statutoriesCount);
        $('.compliance-ck-box-3', clone2).addClass('minus' + count);
        $('.compliance-label-3', clone2).attr('for', 'minus' + statutoriesCount);

        $('.saved', clone2).attr('id', 'save' + statutoriesCount);
        if (value.comp_status > 0 && value.s_s == 1) {
            $('.saved', clone2).addClass('fa-square');
        }

        $('.comp', clone2).on('click', function() {
            compliancestatus(this, value.comp_id, value.u_id, value.level_1_s_id);
        });


        $('#collapse' + count + ' .tbody-compliance-list').append(clone2);

        if (value.comp_status > 0) {
            if (value.comp_status == 1) {
                $('#tick' + statutoriesCount).prop('checked', true);
            } else if (value.comp_status == 2) {
                $('#untick' + statutoriesCount).prop('checked', true);
            } else {
                $('#minus' + statutoriesCount).prop('checked', true);
            }
        }
        statutoriesCount++;
        sno++;
    });

    if (sno <= 1) {
        ShowMore.hide();
        SubmitButton.hide();
        SaveButton.hide();
        var no_record_row = $("#templates .table-no-record tr");
        var no_clone = no_record_row.clone();
        $(".tbody-assignstatutory").append(no_clone);
        $(".total_count_view").hide();
    } else {
        SaveButton.show();
        if (totalRecord == (sno - 1)) {
            SubmitButton.show();
            ShowMore.hide();
        } else {
            SubmitButton.hide();
            ShowMore.show();
        }
        $(".total_count").text('Showing 1 to ' + (sno - 1) + ' of ' + totalRecord + ' entries');
        $(".total_count_view").show();
    }
    hideLoader();
}

function loadMultipleUnitCompliances() {
    var temp1 = "";
    if($('.tbody-assignstatutory tr').last().attr('class') != undefined) {
        var lClass = $('.tbody-assignstatutory tr').last().attr('class').split(' ')[0];
        $('.'+lClass).show();
    }
    
    $.each(COMPLIANCES_LIST, function(key, value) {
        if (LastAct != value.level_1_s_name) {
            var actHeadingRow = $('.mul-act-heading');
            var clone = actHeadingRow.clone();
            $('.panel-title span', clone).text(value.level_1_s_name);
            $('.change_status', clone).attr('id', 'act' + actCount);
            $('.change_status', clone).attr("data-act", actCount);
            $('.change_status', clone).attr("data-act-id", value.level_1_s_id);
            $('.toggle-act', clone).attr('for', actCount);

            $('.r-view', clone).attr('id', 'r-view' + actCount);
            $('.remarks', clone).attr('id', 'remark' + actCount);
            $('.remarks', clone).attr("data-act", actCount);

            if (value.a_status == 2) {
                $('.change_status', clone).html('<img src="images/deletebold.png">').attr('for', '2');
                $('.remarks', clone).attr('value', value.remarks);
                $('.r-view', clone).show();
            } else if (value.a_status == 3) {
                $('.change_status', clone).html('<img src="images/iconminusactive.png">').attr('for', '3');
                $('.remarks', clone).attr('value', value.remarks);
                $('.r-view', clone).show();
            } else {
                $('.change_status', clone).html('<img src="images/tick1bold.png">').attr('for', '1');
            }

            temp1 = temp1 + clone.html();
            var complianceHeadingRow = $('.mul-compliance-heading');
            var clone1 = complianceHeadingRow.clone();
            $('tr', clone1).addClass('act' + actCount);
            temp1 = temp1 + clone1.html();
            count = actCount;
            LastAct = value.level_1_s_name;
            actCount = actCount + 1;
            LastCompliance = "";
        }

        var applUnits = value.applicable_units;
        applcount = 0;
        if(LastCompliance != value.comp_id){
            var complianceDetailtableRow = $('.mul-compliance-details');
            var clone2 = complianceDetailtableRow.clone();

            $('tr', clone2).addClass('act' + count);
            $('.sno', clone2).text(sno);
            $('.statutoryprovision', clone2).text(value.s_provision);
            $('.compliancetask', clone2).text(value.comp_name);
            $('.org-name', clone2).attr('title', 'Organizations: ' + value.org_names);
            $('.compliancedescription', clone2).text(value.descrip);
            $('.applicablelocation', clone2).attr('id', 'appl' + sno);
            $('.applicablelocation', clone2).text(applUnits.length + '/' + ACTIVE_UNITS.length);
            temp1 = temp1 + clone2.html();

            var unitRow = $('.mul-unit-head');
            var clone5 = unitRow.clone();
            $('tr', clone5).addClass('act' + count);
            $('.sub-tick', clone5).attr('id', 'sub-tick-' + sno);
            $('.sub-tick', clone5).attr('name', 'sub-check-' + sno);

            $('.sub-untick', clone5).attr('id', 'sub-untick-' + sno);
            $('.sub-untick', clone5).attr('name', 'sub-check-' + sno);

            $('.sub-minus', clone5).attr('id', 'sub-minus-' + sno);
            $('.sub-minus', clone5).attr('name', 'sub-check-' + sno);

            temp1 = temp1 + clone5.html();

            $(':checkbox').on('change', function() {
                var th = $(this),
                    name = th.attr('name');
                if (th.is(':checked')) {
                    $(':checkbox[name="' + name + '"]').not(th).prop('checked', false);
                }
            });
            sno++;
            LastCompliance = value.comp_id;
        }
        
        var temp = "";
        $.each(applUnits, function(key1, value1) {
            var unitRow = $('.mul-unit-row');
            var clone4 = unitRow.clone();

            if (value1.s_s == 0) {
                $('tr', clone4).addClass('act' + count + ' new_row');
            } else if (value1.s_s == 4) {
                $('tr', clone4).addClass('act' + count + ' rejected_row');
            }else{
                $('tr', clone4).addClass('act' + count);
            }

            var combineId = value.comp_id + '#' + value1.u_id + '#' + value.level_1_s_id + '#' + count;
            $('.combineid-class', clone4).attr('id', 'combineid' + statutoriesCount);
            $('.combineid-class', clone4).val(combineId);

            $('.unit-locatiion', clone4).text(UNIT_CS_ID[value1.u_id].g_name);
            $('.unit-name', clone4).text(UNIT_CS_ID[value1.u_id].unit_code + ' - ' + UNIT_CS_ID[value1.u_id].u_name + ', ' + UNIT_CS_ID[value1.u_id].address);

            $('.compliance-ck-box-1', clone4).attr('name', 'statutory' + statutoriesCount);
            $('.compliance-ck-box-1', clone4).attr('id', 'tick' + statutoriesCount);
            $('.compliance-ck-box-1', clone4).addClass('tick' + count + ' sub-tick-' + (sno - 1));
            $('.compliance-label-1', clone4).attr('for', 'tick' + statutoriesCount);

            $('.compliance-ck-box-2', clone4).attr('name', 'statutory' + statutoriesCount);
            $('.compliance-ck-box-2', clone4).attr('id', 'untick' + statutoriesCount);
            $('.compliance-ck-box-2', clone4).addClass('untick' + count + ' sub-untick-' + (sno - 1));
            $('.compliance-label-2', clone4).attr('for', 'untick' + statutoriesCount);

            $('.compliance-ck-box-3', clone4).attr('name', 'statutory' + statutoriesCount);
            $('.compliance-ck-box-3', clone4).attr('id', 'minus' + statutoriesCount);
            $('.compliance-ck-box-3', clone4).addClass('minus' + count + ' sub-minus-' + (sno - 1));
            $('.compliance-label-3', clone4).attr('for', 'minus' + statutoriesCount);

            if(value1.comp_status > 0){
                if(value1.comp_status == 1){
                    $('.compliance-ck-box-1', clone4).attr('checked', true);
                }else if(value1.comp_status == 2){
                    $('.compliance-ck-box-2', clone4).attr('checked', true);
                }else{
                    $('.compliance-ck-box-3', clone4).attr('checked', true);
                }
            }

            $('.remarks').on('input', function(e) {
                this.value = isCommon($(this));
            });

            $('.saved', clone4).attr('id', 'save' + statutoriesCount);
            if (value1.comp_status > 0 && value1.s_s == 1) {
                $('.saved', clone4).addClass('fa-square');
            }

            temp = temp + clone4.html();
            statutoriesCount++;
        });
        temp1 = temp1 + temp;
    });

    $('.tbody-assignstatutory').append(temp1);

    $( ".change_status" ).unbind( "click" );
    $('.change_status').click(function() {
        if ($(this).attr('for') == "1") {
            $(this).html('<img src="images/deletebold.png">').attr('for', '2');
        } else if ($(this).attr('for') == "2") {
            $(this).html('<img src="images/iconminusactive.png">').attr('for', '3');
        } else {
            $(this).html('<img src="images/tick1bold.png">').attr('for', '1');
        }
        mactstatus(this);
    });

    $( ".comp" ).unbind( "click" );
    $('.comp').on('click', function() {
        mcompliancestatus(this);
    });

    $( ".remarks" ).unbind( "click" );
    $('.remarks').focusout(function() {
        mremarkstatus(this);
    });

    $('.sub-comp').on('click', function() {
        subComplianceStatus(this);
    });

    if (sno <= 1) {
        ShowMore.hide();
        SubmitButton.hide();
        SaveButton.hide();
        var no_record_row = $("#templates .table-no-record tr");
        var no_clone = no_record_row.clone();
        $(".tbody-assignstatutory").append(no_clone);
        $(".total_count_view").hide();
    } else {
        SaveButton.show();
        if (totalRecord == (sno - 1)) {
            SubmitButton.show();
            ShowMore.hide();
        } else {
            SubmitButton.hide();
            ShowMore.show();
        }
        $(".total_count").text('Showing 1 to ' + (sno - 1) + ' of ' + totalRecord + ' entries');
        $(".total_count_view").show();
    }
    hideLoader();
}

function showList() {
    CURRENT_TAB = 1;
    AssignStatutoryView.show();
    AssignStatutoryAdd.hide();
    callAPI(API_LIST);
}

function ifNullReturnHyphen(value) {
    if (value) {
        return value;
    } else {
        return "-";
    }
}

function loadAssignedStatutories() {
    var sno_ = 0;
    ACTIVE_UNITS = [];
    UNIT_CS_ID = {};

    AssignedStatutoryList.empty();
    $.each(ASSIGNED_STATUTORIES, function(key, value) {
        ++sno_;

        var clone = AssignedStatutoryRow.clone();
        if (value.approval_status_text == 'Rejected') {
            clone.addClass('rejected_row');
        }
        $(TblSno, clone).text(sno_);
        $(TblCountry, clone).text(value.c_name);
        $(TblGroup, clone).text(value.grp_name);
        $(TblBG, clone).text(value.b_grp_name);
        $(TblLE, clone).text(value.l_e_name);
        $(TblDiv, clone).text(ifNullReturnHyphen(value.div_name));
        $(TblCat, clone).text(ifNullReturnHyphen(value.cat_name));
        $(TblLoc, clone).text(value.g_name);
        $(TblUnit, clone).text(value.u_name);
        $(TblDomain, clone).text(value.d_name);

        var status_text = value.approval_status_text;
        if (value.is_editable == false) {
            status_text = 'Assigned';
        }

        if (value.approval_status_text != 'Rejected') {
            $(TblStatus, clone).text(status_text);
        } else {
            $(TblStatus, clone).html('<i class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="' + value.reason + '"></i>' + value.approval_status_text);
        }

        if (value.is_editable) {
            $('.edit-icon', clone).addClass('fa fa-pencil text-primary c-pointer');
            $('.edit-icon', clone).on('click', function() {
                LastAct = '';
                LastSubAct = '';
                GroupName.val(value.grp_name);
                BusinessGroupName.val(value.b_grp_name);
                LegalEntityName.val(value.l_e_name);
                DivisionName.val(value.div_name);
                CategoryName.val(value.cat_name);
                DomainName.val(value.d_name);
                val_group_id = value.ct_id.toString();
                val_domain_id = value.d_id.toString();
                val_legal_entity_id = value.le_id.toString();
                CLIENT_STATUTORY_ID = value.client_statutory_id;
                UNIT_TEXT = value.u_name;
                DOMAIN_TEXT = value.d_name;
                ACTIVE_UNITS = [value.u_id];
                EditAssignedStatutory();
            });
        }

        AssignedStatutoryList.append(clone);
    });

    if(sno_ == 0){
        var no_record_row = $("#templates .table-no-record tr");
        var no_clone = no_record_row.clone();
        AssignedStatutoryList.append(no_clone);
    }
    hideLoader();
}

function validateFirstTab() {
    if (ACTIVE_UNITS.length <= 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
        $(".total_count_view").hide();
        LastAct = '';
        LastSubAct = '';
        statutoriesCount = 1;
        actCount = 1;
        count = 1;
        sno = 1;
        totalRecord = 0;
        AssignStatutoryList.empty();
        SingleAssignStatutoryList.empty();
        SELECTED_COMPLIANCE = {};
        ACT_MAP = {};
        return true;
    }
};

function showTab() {
    hideall = function() {
        // $('.setup-panel li').addClass('disabled');
        $('.statutory_mapping_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();
        ShowMore.hide();
        SaveButton.hide();
        SubmitButton.hide();
        NextButton.hide();
        PreviousButton.hide();
    }

    enabletabevent = function(tab) {
        if (tab == 1) {
            $('.tab-step-1 a').attr('href', '#tab1');
        } else if (tab == 2) {
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
    } else if (CURRENT_TAB == 2) {
        if (validateFirstTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {
            displayLoader();
            mirror.getAssignStatutoryWizardTwoCount(
                int(val_domain_id), ACTIVE_UNITS,
                function(error, data) {
                    if (error == null) {
                        totalRecord = data.total_records;
                        if (data.unit_total > 5000 && ACTIVE_UNITS.length > 1) {
                            displayMessage(message.maximum_compliance_selection_reached);
                            hideLoader();
                            CURRENT_TAB -= 1;
                            return false;
                        } else {
                            callAPI(API_Wizard2);
                            hideall();
                            enabletabevent(2);
                            $('.tab-step-2').addClass('active')
                            $('#tab2').addClass('active in');
                            $('#tab2').show();
                            SubmitButton.show();
                            PreviousButton.show();
                            SaveButton.show();
                            ShowMore.show();
                            showBreadCrumbText();
                        }
                    } else {
                        displayMessage(error);
                        hideLoader();
                        CURRENT_TAB -= 1;
                        return false;
                    }
                }
            );
        }
    }
};


function EditAssignedStatutory() {
    displayLoader();
    $(".total_count_view").hide();
    LastAct = '';
    LastSubAct = '';
    statutoriesCount = 1;
    actCount = 1;
    count = 1;
    sno = 1;
    totalRecord = 0;
    AssignStatutoryList.empty();
    SingleAssignStatutoryList.empty();
    SELECTED_COMPLIANCE = {};
    ACT_MAP = {};

    mirror.getAssignStatutoryWizardTwoCount(
        int(val_domain_id), ACTIVE_UNITS,
        function(error, data) {
            if (error == null) {
                totalRecord = data.total_records;
                AssignStatutoryView.hide();
                AssignStatutoryAdd.show();
                $('.statutory_mapping_tab li').removeClass('active');
                $('.tab-pane').removeClass('active in');
                $('#tab1').hide();
                PreviousButton.hide();
                NextButton.hide();
                $('.tab-step-2 a').attr('href', '#tab2');
                $('.tab-step-2').addClass('active')
                $('#tab2').addClass('active in');
                $('#tab2').show();
                showBreadCrumbText();
                callAPI(API_Wizard2);
            } else {
                displayMessage(error);
                hideLoader();
            }
        }
    );
}

function initialize() {
    pageControls();
    showList();
}

function showhide(ele) {
    var id = $(ele).attr('for');
    $('.act'+id).toggle();
}

$(function() {
    $('html').offset().top;
    initialize();
    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
    $(".table-fixed").stickyTableHeaders();
});
