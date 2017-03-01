/* Elements */
var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var CancelButton = $('#btn-cancel');
var StatutorySettingsView = $("#statutorysettings-view");
var StatutorySettingsAdd = $("#statutorysettings-add");
var Show = $(".btn-show");
var ShowMore = $(".btn-showmore");
var EditButton = $('.btn-edit');
var PasswordSubmitButton = $('#password-submit');

var CurrentPassword = $('#current-password');

var SubmitButton = $("#btn-submit");
var SaveButton = $("#btn-save");

var BusinessGroupNameLabel = $(".business-group-name");
var BusinessGroupNameAC = $(".business-group-name-ac");

var BusinessGroupName = $("#business_group_name");
var BusinessGroupId = $("#business_group_id");
var ACBusinessGroup = $("#ac-business-group");

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var DivisionName = $("#division_name");
var DivisionId = $("#division_id");
var ACDivision = $("#ac-division");

var CategoryName = $("#category_name");
var CategoryId = $("#category_id");
var ACCategory = $("#ac-category");

var UnitRow = $("#templates .unit-row li");
var UnitList = $(".unit-list");
var SelectAll = $('#unit-checkbox-main');
var SelectedUnitCount = $(".selected_checkbox_count");
var SelectedUnitView = $(".selected_checkbox");

var AssignStatutoryList = $(".tbody-assignstatutory");
var SingleAssignStatutoryList = $(".tbody-single-assignstatutory");
var StatutoryProvision = ".statutoryprovision";
var ComplianceTask = ".compliancetask";
var ComplianceDescription = ".compliancedescription";

var StatutorySettingsList = $(".tbody-statutorysettings-list");
var StatutorySettingsRow = $("#templates .table-statutorysettings .table-row");

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
var BUSINESS_GROUPS = null;
var DIVISIONS = null;
var CATEGORIES = null;
var UNITS = null;
var COMPLIANCES_LIST = null;
var ASSIGNED_STATUTORIES = null;

/* Values */
var val_business_group_id = null;
var val_legal_entity_id = null;
var val_division_id = null;
var val_category_id = null;
var val_unit_id = null;
var ACTIVE_UNITS = [];
var DOMAIN_ID = null;
var UNIT_CS_ID = {};
var CLIENT_STATUTORY_ID = null;
var UNIT_TEXT = null;
var DOMAIN_TEXT = null;
var TOTAL_COMPLIANCE = 0;

/* API Types */
var API_FILTERS = 'filter';
var API_Wizard1 = "wizard_1";
var API_Wizard2 = "wizard_2";
var SAVE_API = "save";
var SUBMIT_API = "submit";
var API_LIST = "list";
var EDIT_API = "edit";
var LOCK_API = "lock";

var LastAct = '';
var LastSubAct = '';
var statutoriesCount = 1;
var actCount = 1;
var count = 1;
var sno = 1;
var totalRecord = 0;

AssignStatutoryList.empty();
SingleAssignStatutoryList.empty();
var SELECTED_COMPLIANCE = {};
var ACT_MAP = {};
var isAuthenticate;
var C_COUNT = 0;

var L_DOMAIN = '';
var L_UNIT = '';
var L_STATUS = '';

function callAPI(api_type) {
    if (api_type == API_FILTERS) {
        displayLoader();
        client_mirror.getStatutorySettingsFilters(function(error, data) {
            if (error == null) {
                DIVISIONS = data.div_infos;
                CATEGORIES = data.cat_info;
                //loadAssignedStatutories();
                
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == API_Wizard1) {
        displayLoader();
        client_mirror.getStatutorySettingsCompliance(parseInt(LegalEntityId.val()), ACTIVE_UNITS, (sno - 1), DOMAIN_ID, function(error, data) {
            if (error == null) {
                COMPLIANCES_LIST = data.applicable_statu;
                totalRecord = data.r_count;
                if (ACTIVE_UNITS.length == 1) {
                    loadSingleUnitCompliances();
                } else {
                    loadMultipleUnitCompliances();
                }
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == LOCK_API) {
        displayLoader();
        client_mirror.changeStatutorySettingsLock(parseInt(LegalEntityId.val()), L_DOMAIN, L_UNIT, L_STATUS,
            CurrentPassword.val(), function(error, data) {
            if (error == null) {
                reset();
                loadEntityDetails();
                hideLoader();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == SAVE_API || api_type == SUBMIT_API) {

        //check request is save or submit
        var submission_status;
        if (api_type == SAVE_API) {
            submission_status = 1;
        } else {
            submission_status = 2;
        }

        var checkSubmit = true;
        //check all compliance is selected before submit
        /*var checkSubmit = false;
        if($('.comp:checked').length == (statutoriesCount - 1)){
            checkSubmit = true;
        }*/

        //check remark validation
        /*for(var i=1; i<=(actCount-1); i++){
            var aStatus = parseInt($('#act'+i).attr("for"));
            var remark = null;
            if(aStatus == 2 || aStatus==3){
                remark = $('#remark'+i).val().trim();
                if(remark==''){
                    displayMessage(message.remarks_required);
                    hideLoader();
                    return false;
                }
            }
        }*/
        
        var selected_compliances_list = [];
        $.each(SELECTED_COMPLIANCE, function(key, value) {
            selected_compliances_list.push(
                value
            );
        });

        client_mirror.updateStatutorySettings(CurrentPassword.val(), selected_compliances_list, parseInt(LegalEntityId.val()), submission_status,
            DOMAIN_ID, ACTIVE_UNITS,
            function(error, data) {
                if (error == null) {
                    if (submission_status == 1) {
                        displaySuccessMessage(message.save_success);
                    } else {
                        displaySuccessMessage(message.submit_success);
                    }
                    reset();
                    StatutorySettingsView.show();
                    StatutorySettingsAdd.hide();
                    loadEntityDetails();
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            }
        );

        /*if (submission_status == 1 && selected_compliances_list.length == 0) {
            displayMessage(message.nocompliance_selected_forassign);
            hideLoader();
            return false;
        }
        else if (submission_status == 2 && checkSubmit == false) {
            displayMessage(message.assigncompliance_submit_failure);
            hideLoader();
            return false;
        } else {
            client_mirror.updateStatutorySettings('pass@123', selected_compliances_list, parseInt(LegalEntityId.val()), submission_status,
                DOMAIN_ID, ACTIVE_UNITS,
                function(error, data) {
                    if (error == null) {
                        if (submission_status == 1) {
                            displaySuccessMessage(message.save_success);
                        } else {
                            displaySuccessMessage(message.submit_success);
                        }
                        reset();
                        StatutorySettingsView.show();
                        StatutorySettingsAdd.hide();
                        loadEntityDetails();
                        hideLoader();
                    } else {
                        displayMessage(error);
                        hideLoader();
                    }
                }
            );
        }*/
    }
}


function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'business_group_id') {
        LegalEntityName.val('');
        LegalEntityId.val('');
        DivisionName.val('');
        DivisionId.val('');
        CategoryName.val('');
        CategoryId.val('');
    } else if (current_id == 'legal_entity_id') {
        DivisionName.val('');
        DivisionId.val('');
        CategoryName.val('');
        CategoryId.val('');
    } else if (current_id == 'division_id') {
        CategoryName.val('');
        CategoryId.val('');
    }
    /*UnitList.empty();
    ACTIVE_UNITS = [];*/
}

//validate
function validateAuthentication() {
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    } else {
        isAuthenticate = true;
        Custombox.close();
    }
    displayLoader();
   /* mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            isAuthenticate = true;
            Custombox.close();
        } else {
            hideLoader();
            displayMessage(error);
            CurrentPassword.val('');
            CurrentPassword.focus();
        }
    });*/
}

function pageControls() {
    Show.click(function() {
        validateAndShow();
    });

    SelectAll.change(function() {
        ACTIVE_UNITS = [];
        C_COUNT = 0;
        DOMAIN_ID = null;
        //UNIT_CS_ID = {};
        if (UNITS.length > 0) {
            $(".tbody-statutorysettings-list .unit-checkbox").prop('checked', $(this).prop("checked"));

            $('.tbody-statutorysettings-list .unit-checkbox').each(function(index, el) {
                if (SelectAll.prop('checked')) {
                    var chkid = $(el).val().split(',');
                    ACTIVE_UNITS.push(parseInt(chkid[0]));
                    C_COUNT = C_COUNT + chkid[2];

                    if(C_COUNT > 5000){
                        displayMessage(message.maximum_compliance_selection_reached_select_all);
                        return false;
                    }
                    else if (ACTIVE_UNITS.length >= 20) {
                        displayMessage(message.maximum_units);
                        return false;
                    } else {
                        if(DOMAIN_ID == null || DOMAIN_ID == chkid[1]){
                            $(this).prop("checked", true);
                            DOMAIN_ID = parseInt(chkid[1]);
                        }else{
                            $(this).prop("checked", false);
                        }
                    }
                } else {
                    $(this).prop("checked", false);
                }
            });
            SelectedUnitCount.text(ACTIVE_UNITS.length);
        }
    });

    EditButton.click(function() {
        //reset();
        sno = 1;
        statutoriesCount = 1;
        $(".total_count_view").hide();
        $('.tbody-compliance-list').empty();
        ShowMore.hide();
        SaveButton.hide();
        SubmitButton.hide();
        StatutorySettingsView.hide();
        StatutorySettingsAdd.show();
        callAPI(API_Wizard1);
    });

    CancelButton.click(function() {
        StatutorySettingsView.show();
        StatutorySettingsAdd.hide();
        reset();
    });

    BusinessGroupName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACBusinessGroup, BusinessGroupId, text_val,
            LEGAL_ENTITIES, "bg_name", "bg_id",
            function(val) {
                onAutoCompleteSuccess(BusinessGroupName, BusinessGroupId, val);
            });
    });

    LegalEntityName.keyup(function(e) {
        var condition_fields = [];
        var condition_values = [];
        if (BusinessGroupId.val() != '') {
            condition_fields.push("bg_id");
            condition_values.push(BusinessGroupId.val());
        }
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACLegalEntity, LegalEntityId, text_val,
            LEGAL_ENTITIES, "le_name", "le_id",
            function(val) {
                onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
            }, condition_fields, condition_values);
        
    });

    DivisionName.keyup(function(e) {
        if (LegalEntityId.val() != '') {
            var condition_fields = ["le_id"];
            var condition_values = [LegalEntityId.val()];
            if (BusinessGroupId.val() != '') {
                condition_fields.push("bg_id");
                condition_values.push(BusinessGroupId.val());
            }
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACDivision, DivisionId, text_val,
                DIVISIONS, "div_name", "div_id",
                function(val) {
                    onAutoCompleteSuccess(DivisionName, DivisionId, val);
                }, condition_fields, condition_values);
        }
    });

    CategoryName.keyup(function(e) {
        if (LegalEntityId.val() != '') {
            var condition_fields = ["legal_entity_id"];
            var condition_values = [LegalEntityId.val()];
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

    ShowMore.click(function() {
        callAPI(API_Wizard1);
    });

    SubmitButton.click(function() {
        displayPopUp(SUBMIT_API, null);
        /*displayLoader();
        setTimeout(function() {
            callAPI(SUBMIT_API)
        }, 500);*/
    });

    SaveButton.click(function() {
        displayPopUp(SAVE_API, null);
    });

    PasswordSubmitButton.click(function() {
        validateAuthentication();
    });
}


function reset() {
    LastAct = '';
    AssignStatutoryList.empty();
    SingleAssignStatutoryList.empty();
    ACTIVE_UNITS = [];
    C_COUNT = 0;
    DOMAIN_ID = null;
    SELECTED_COMPLIANCE = {};
    SelectAll.prop("checked", false);
    $(".tbody-statutorysettings-list .unit-checkbox").prop('checked', false);
    SelectedUnitCount.text(ACTIVE_UNITS.length);
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
function c_bool(value) {
    if(value == 1){
        return true;
    }else{
        return false;
    }
}

function validateAndShow() {
    val_business_group_id = BusinessGroupId.val();
    val_legal_entity_id = LegalEntityId.val();
    val_division_id = DivisionId.val();
    val_category_id = CategoryId.val();
    
    if (val_legal_entity_id.trim().length <= 0) {
        SelectedUnitView.hide();
        EditButton.hide();
        displayMessage(message.legalentity_required);
        return false;
    } else {
        displayLoader();
        client_mirror.getStatutorySettings(int(val_legal_entity_id), int(val_division_id), int(val_category_id),
            function(error, data) {
                if (error == null) {
                    UNITS = data.statutories;
                    loadUnits();
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
        });
    }
}

/*function displayLockPopUp(UID){
    Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
        complete: function() {
            CurrentPassword.focus();
            CurrentPassword.val('');
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
                mirror.approveAssignedStatutory(UNIT_ID, DOMAIN_ID, CLIENT_STATUTORY_ID, REJ_COMP,
                parseInt(approval_status), reason, UNIT_TEXT, DOMAIN_TEXT,
                    function(error, data) {
                        if (error == null) {
                            $(".total_count_view").hide();
                            displaySuccessMessage(message.action_success);
                            Show.trigger( "click" );
                        } else {
                            hideLoader();
                            displayMessage(error);
                        }
                    }
                );
            }
        },
    });
}*/

function displayPopUp(TYPE, LOCK_ARRAY){
    Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
        complete: function() {
            CurrentPassword.focus();
            CurrentPassword.val('');
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
                displayLoader();
                setTimeout(function() {
                    if(TYPE == LOCK_API){
                        L_UNIT = parseInt(LOCK_ARRAY[0]);
                        L_DOMAIN = parseInt(LOCK_ARRAY[1]);
                        if(LOCK_ARRAY[2] == true){
                            L_STATUS = false;
                        }else{
                            L_STATUS = true;
                        }
                        callAPI(TYPE);
                    }else{
                        callAPI(TYPE);
                    }
                }, 500);
            }
        },
    });
}

function activateUnit(element) {
    var chkid = $(element).val().split(',');
    if ($(element).prop("checked")) {
        if(C_COUNT > 5000){
            displayMessage(message.maximum_compliance_selection_reached_select_all);
            return false;
        }
        else if (ACTIVE_UNITS.length >= 20) {
            displayMessage(message.maximum_units);
            return false;
        }else{
            if(DOMAIN_ID == null || DOMAIN_ID == chkid[1]){
                $(this).prop("checked", true);
                DOMAIN_ID = parseInt(chkid[1]);
                ACTIVE_UNITS.push(parseInt(chkid[0]));
                C_COUNT = C_COUNT + chkid[2];
            }else{
                displayMessage(message.unit_selection_should_be_same_domain);
            }
        }
    } else {
        index = ACTIVE_UNITS.indexOf(parseInt(chkid[0]));
        ACTIVE_UNITS.splice(index, 1);
        C_COUNT = C_COUNT - chkid[2];
    }
    SelectedUnitCount.text(ACTIVE_UNITS.length);
}

function loadUnits() {
    C_COUNT = 0;
    UNIT_CS_ID = {};
    StatutorySettingsList.empty();
    $.each(UNITS, function(key, value) {
        var upd_by = '-';
        if(value.usr_by != null){
            upd_by = value.usr_by;
        }
        var upd_on = '-';
        if(value.usr_on != null){
            upd_on = value.usr_on;
        }

        var clone = StatutorySettingsRow.clone();
        if(value.is_new){
            clone.addClass('new_row');
        }

        $('.unit-checkbox', clone).attr('id', 'unit' + key);
        $('.unit-checkbox', clone).val(value.u_id + ',' + value.d_id + ',' + value.r_count);

        $('.tbl_unit', clone).text(value.u_name);
        $('.tbl_location', clone).text(value.address);
        $('.tbl_domain', clone).text(value.d_name);
        $('.tbl_no_of_compliance', clone).text(value.r_count);
        $('.tbl_updated_by', clone).text(upd_by);
        $('.tbl_updated_on', clone).text(upd_on);
        if(value.is_locked){
            $('.tbl_lock', clone).find('i').addClass('fa-lock');
        }else{
            $('.tbl_lock', clone).find('i').addClass('fa-unlock');
        }

        $('.tbl_lock', clone).click(function() {
            if(value.allow_unlock == true){
                //displayLockPopUp(value.u_id);
                displayPopUp(LOCK_API, [value.u_id, value.d_id, value.is_locked]);
            }else{
                displayMessage(message.unlock_permission);
            }
        });

        $('.unit-checkbox', clone).on('click', function(e) {
            activateUnit(this);
        });

        StatutorySettingsList.append(clone);

        UNIT_CS_ID[value.u_id] = {
            'u_name': value.u_name,
            'u_address': value.address
        }

    });

    if(UNITS.length == 0){
        SelectedUnitView.hide();
        EditButton.hide();
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        StatutorySettingsList.append(clone);
    }else{
        SelectedUnitView.show();
        EditButton.show();
    }
   
}

/*
function loadUnits() {
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
}*/

function actstatus(element) {
    var checkedVal = parseInt($(element).attr("for"));
    var remarkbox = '#r-view' + $(element).val();
    var A_REMARK = null;

    if (checkedVal > 1) {
        $(remarkbox).show();
        if($('#remark' + $(element).val()).val() != ''){
            A_REMARK = $('#remark' + $(element).val()).val();
        }
    } else {
        $(remarkbox).hide();
    }

    var currentAction = '.comp' + $(element).val();
    $(currentAction).each(function() {
        var C_S_ID = null;
        if (checkedVal > 1) {
            $(this).html('<img src="images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="images/tick-orange.png">').attr('for', '1');
        }
        var sid = $(this).val();
        $('#save' + sid).addClass('fa-square');

        var combine_ids = $('#combineid' + sid).val().split('#');
        SELECTED_COMPLIANCE[combine_ids[0]] = {
            'c_c_id': parseInt(combine_ids[2]),
            'a_status': c_bool(checkedVal),
            'n_a_remarks': A_REMARK,
            'comp_id': parseInt(combine_ids[0]),
            'c_o_status': c_bool(checkedVal),
            'c_remarks': null,
            'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
            'u_id': parseInt(combine_ids[1])
        }
        console.log(SELECTED_COMPLIANCE)
    });
}

function remarkstatus(element) {
    var ID = $(element).attr("data-act");
    var A_STATUS = parseInt($('#act' + ID).attr("for"));
    var A_REMARK = null;
    if($(element).val() != ''){
        A_REMARK = $(element).val();
    }

    var currentAction = '.comp' + ID;
    $(currentAction).each(function() {
        var C_S_ID = null;
        var sid = $(this).val();

        var combine_ids = $('#combineid' + sid).val().split('#');
        /*if (CLIENT_STATUTORY_ID == null) {
            C_S_ID = UNIT_CS_ID[combine_ids[1]].client_statutory_id;
            UNIT_TEXT = UNIT_CS_ID[combine_ids[1]].unit_code + ' - ' + UNIT_CS_ID[combine_ids[1]].u_name;
        }else{
            C_S_ID = CLIENT_STATUTORY_ID;
        }*/

        var C_STATUS = parseInt($(this).attr("for"));
       
        if (C_STATUS > 1) {
            SELECTED_COMPLIANCE[combine_ids[0]] = {
                'c_c_id': parseInt(combine_ids[2]),
                'a_status': c_bool(A_STATUS),
                'n_a_remarks': A_REMARK,
                'comp_id': parseInt(combine_ids[0]),
                'c_o_status': c_bool(C_STATUS),
                'c_remarks': null,
                'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
                'u_id': parseInt(combine_ids[1])
            }
        }
    });
    console.log(SELECTED_COMPLIANCE);
}

function compliancestatus(element, C_ID, U_ID, A_ID) {
    var C_S_ID = null;
    var sid = $(element).val();
    $('#save' + sid).addClass('fa-square');

    var applicable = $(element).attr("data-applicable");

    var combine_ids = $('#combineid' + sid).val().split('#');

    var A_STATUS = $('#act' + combine_ids[3]).attr("for");
    var A_REMARK = null;
    
    var C_STATUS = parseInt($(element).attr("for"));
    if (C_STATUS > 1 && $('#remark' + combine_ids[3]).val() != '') {
        A_REMARK = $('#remark' + combine_ids[3]).val();
    }
    SELECTED_COMPLIANCE[combine_ids[0]] = {
        'c_c_id': parseInt(combine_ids[2]),
        'a_status': c_bool(A_STATUS),
        'n_a_remarks': A_REMARK,
        'comp_id': parseInt(combine_ids[0]),
        'c_o_status': c_bool(C_STATUS),
        'c_remarks': null,
        'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
        'u_id': parseInt(combine_ids[1])
    }
    console.log(SELECTED_COMPLIANCE);
}

function mactstatus(element) {
    //var A_ID = parseInt($(element).attr("data-act-id"));
    var ID = $(element).attr("data-act");

    var checkedVal = parseInt($(element).attr("for"));

    var remarkbox = '#r-view' + ID;
    var A_REMARK = null;

    if (checkedVal > 1) {
        $(remarkbox).show();
        if($('#remark' + ID).val() != ''){
            A_REMARK = $('#remark' + ID).val();
        }
    } else {
        $(remarkbox).hide();
    }

    var currentAction = '.comp' + ID;

    $(currentAction).each(function() {
        var C_S_ID = null;

        if (checkedVal > 1) {
            $(this).html('<img src="images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="images/tick-orange.png">').attr('for', '1');
        }

        var sname = $(this).attr('id');
        var sid = sname.substr(sname.lastIndexOf('p') + 1);
        //$('#save' + sid).addClass('fa-square');

        var combine_ids = $('#combineid' + sid).val().split('#');
        /*if (CLIENT_STATUTORY_ID == null) {
            C_S_ID = UNIT_CS_ID[combine_ids[1]].client_statutory_id;
            UNIT_TEXT = UNIT_CS_ID[combine_ids[1]].unit_code + ' - ' + UNIT_CS_ID[combine_ids[1]].u_name;
        }else{
            C_S_ID = CLIENT_STATUTORY_ID;
        }*/
        var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
        SELECTED_COMPLIANCE[C_U_ID] = {
            'c_c_id': parseInt(combine_ids[2]),
            'a_status': c_bool(checkedVal),
            'n_a_remarks': A_REMARK,
            'comp_id': parseInt(combine_ids[0]),
            'c_o_status': c_bool(checkedVal),
            'c_remarks': null,
            'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
            'u_id': parseInt(combine_ids[1])
        }
    });
    console.log(SELECTED_COMPLIANCE)
}

function mcompliancestatus(element) {
    var C_S_ID = null;
    /*var sname = $(element).attr('class');
    var sid = sname.substr(sname.lastIndexOf('-') + 1);
    $('#save' + sid).addClass('fa-square');*/

    var sname1 = $(element).attr('id');
    var sid1 = sname1.substr(sname1.lastIndexOf('p') + 1);

    var combine_ids = $('#combineid' + sid1).val().split('#');
    var C_ID = combine_ids[0];
    var U_ID = combine_ids[1];
    var C_C_ID = combine_ids[2];
    var ID = combine_ids[3];

    var A_STATUS = $('#act' + ID).attr("for");
    var A_REMARK = null;
    var C_STATUS = parseInt( $(element).attr('for'));
    if (C_STATUS > 1 && $('#remark' + ID).val() != '') {
        A_REMARK = $('#remark' + ID).val();
    }
    /*if (CLIENT_STATUTORY_ID == null) {
        C_S_ID = UNIT_CS_ID[U_ID].client_statutory_id;
        UNIT_TEXT = UNIT_CS_ID[U_ID].unit_code + ' - ' + UNIT_CS_ID[U_ID].u_name;
    }else{
        C_S_ID = CLIENT_STATUTORY_ID;
    }*/

    var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
    SELECTED_COMPLIANCE[C_U_ID] = {
        'c_c_id': parseInt(combine_ids[2]),
        'a_status': c_bool(A_STATUS),
        'n_a_remarks': A_REMARK,
        'comp_id': parseInt(combine_ids[0]),
        'c_o_status': c_bool(C_STATUS),
        'c_remarks': null,
        'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
        'u_id': parseInt(combine_ids[1])
    }
    console.log(SELECTED_COMPLIANCE);
}

/*
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

    if ($(element).is(':checked')) {
        $('#save' + sid).removeClass('fa-square');
        $('.' + id).each(function() {
            var C_S_ID = null;
            $(this).prop("checked", true);
            var C_STATUS = parseInt($(this).val());

            var sname = $(this).attr('name');
            var sid = sname.substr(sname.lastIndexOf('y') + 1);

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

    
}
*/

function part_compliance(remark) {
  if (remark.length > 15) {
    return remark.substring(0, 10) + '...';
  } else {
    return remark;
  }
}

function loadSingleUnitCompliances() {

    $.each(COMPLIANCES_LIST, function(key, value) {
        if (LastAct != value.lone_statu_name) {
            var acttableRow = $('#act-templates .p-head');
            var clone = acttableRow.clone();

            $('.acc-title', clone).attr('id', 'heading' + actCount);
            $('.panel-title a span', clone).text(value.lone_statu_name);
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

            if (value.opt_status) {
                $('#act' + actCount).html('<img src="images/tick1bold.png">').attr('for', '1');
            } else {
                $('#act' + actCount).html('<img src="images/deletebold.png">').attr('for', '2');
                $('#remark' + actCount).val(value.not_app_remarks);
                $('#r-view' + actCount).show();
            }

            $('#act' + actCount).click(function() {
                if ($(this).attr('for') == "1") {
                    $(this).html('<img src="images/deletebold.png">').attr('for', '2');
                } else {
                    $(this).html('<img src="images/tick1bold.png">').attr('for', '1');
                }
                actstatus(this);
                //actstatus(this, value.level_1_s_id);
            });

            $('#remark' + actCount).focusout(function() {
                remarkstatus(this);
            });

            $('.remarks').on('input', function(e) {
                this.value = isCommon($(this));
            });

            count = actCount;
            LastAct = value.lone_statu_name;
            LastSubAct = "";
            actCount = actCount + 1;
        }

        var applUnits = value.unit_wise_status;
        $.each(applUnits, function(key1, value1) {
            var complianceDetailtableRow = $('#statutory-value .table-statutory-values .compliance-details');
            var clone2 = complianceDetailtableRow.clone();
            var combineId = value.comp_id + '#' + value1.unit_id + '#' + value1.c_comp_id + '#' + count;
            $('.combineid-class', clone2).attr('id', 'combineid' + statutoriesCount);
            $('.combineid-class', clone2).val(combineId);

            if (value1.is_new) {
                clone2.addClass('new_row');
            }

            $('.sno', clone2).text(statutoriesCount);
            $('.statutoryprovision', clone2).text(value.s_prov);
            $('.compliancetask', clone2).text(value.comp_name);
            $('.org-name', clone2).attr('title', value.comp_name);
            $('.compliancefrequency', clone2).text('Frequency');
            $('.compliancedescription', clone2).text(value.descp);


            if(value1.comp_app_status){
                $('.applicable', clone2).html('<img src="images/tick1bold.png">');
            }else{
                $('.applicable', clone2).html('<img src="images/deletebold.png">');
            }

            $('.opted', clone).attr("data-applicable", value1.comp_app_status);
            $('.opted', clone2).attr('id', 'comp' + statutoriesCount);
            $('.opted', clone2).val(statutoriesCount);
            $('.opted', clone2).addClass('comp' + count);

            $('.c-remark-view', clone).attr('id', 'c-remark-view-' + statutoriesCount);
            $('.c-remark-add', clone).attr('id', 'c-remark-add-' + statutoriesCount);
            if(value1.comp_remarks != null){
                $('.c-remark-view i', clone2).attr('title', value1.comp_remarks);
                $('.c-remark-view span', clone2).text(part_compliance(value1.comp_remarks));
            }else{
                $('.c-remark-view', clone2).hide();
            }
            $('.saved', clone2).attr('id', 'save' + statutoriesCount);
            if (value1.is_saved) {
                $('.saved', clone2).addClass('fa-square');
            }

            $('.opted', clone2).on('click', function() {
                if ($(this).attr('for') == "1") {
                    $(this).html('<img src="images/deletebold.png">').attr('for', '2');
                } else {
                    $(this).html('<img src="images/tick-orange.png">').attr('for', '1');
                }
                compliancestatus(this, value.comp_id, value.u_id, value.level_1_s_id);
            });

            
            $('#collapse' + count + ' .tbody-compliance-list').append(clone2);

            if (value1.comp_opt_status) {
                $('#comp' + statutoriesCount).html('<img src="images/tick-orange.png">').attr('for', '1');
            } else {
                $('#comp' + statutoriesCount).html('<img src="images/deletebold.png">').attr('for', '2');
                /*$('#remark' + actCount).val(value.remarks);
                $('#r-view' + actCount).show();*/
            }

            /*$('#comp' + statutoriesCount).click(function() {
                if ($(this).attr('for') == "1") {
                    $(this).html('<img src="images/deletebold.png">').attr('for', '2');
                } else {
                    $(this).html('<img src="images/tick-orange.png">').attr('for', '1');
                }
            });*/
            
            statutoriesCount++;
            sno++;

            if(value1.is_saved == false){
                SELECTED_COMPLIANCE[value.comp_id] = {
                    'c_c_id': value1.c_comp_id,
                    'a_status': c_bool(value.opt_status),
                    'n_a_remarks': value.not_app_remarks,
                    'comp_id': value.comp_id,
                    'c_o_status': c_bool(value1.comp_opt_status),
                    'c_remarks': null,
                    'u_name': UNIT_CS_ID[value1.unit_id].u_name,
                    'u_id': value1.unit_id
                }
                console.log(SELECTED_COMPLIANCE);
            }
        });
        
    });
    if (sno <= 0) {
        SubmitButton.hide();
        SaveButton.hide();
        var no_record_row = $("#templates .table-no-record tr");
        var no_clone = no_record_row.clone();
        $(".tbody-compliance-list").append(no_clone);
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
    $.each(COMPLIANCES_LIST, function(key, value) {
        if (LastAct != value.lone_statu_name) {
            var actHeadingRow = $('.mul-act-heading');
            var clone = actHeadingRow.clone();
            $('.panel-title span', clone).text(value.lone_statu_name);
            $('.change_status', clone).attr('id', 'act' + actCount);
            $('.change_status', clone).attr("data-act", actCount);
            //$('.change_status', clone).attr("data-act-id", value.level_1_s_id);
            $('.toggle-act', clone).attr('for', actCount);

            $('.r-view', clone).attr('id', 'r-view' + actCount);
            $('.remarks', clone).attr('id', 'remark' + actCount);
            $('.remarks', clone).attr("data-act", actCount);

            if (value.opt_status) {
                $('.change_status', clone).html('<img src="images/tick1bold.png">').attr('for', '1');
            } else {
                $('.change_status', clone).html('<img src="images/deletebold.png">').attr('for', '2');
                $('.remarks', clone).attr('value', value.not_app_remarks);
                $('.r-view', clone).show();
            }

            temp1 = temp1 + clone.html();
            var complianceHeadingRow = $('.mul-compliance-heading');
            var clone1 = complianceHeadingRow.clone();
            $('tr', clone1).addClass('act' + actCount);
            temp1 = temp1 + clone1.html();
            count = actCount;
            LastAct = value.lone_statu_name;
            actCount = actCount + 1;
        }

        applcount = 0;
        var complianceDetailtableRow = $('.mul-compliance-details');
        var clone2 = complianceDetailtableRow.clone();
        
        $('tr', clone2).addClass('act' + count);
        $('.sno', clone2).text(sno);
        $('.statutoryprovision', clone2).text(value.s_prov);
        $('.compliancetask', clone2).text(value.comp_name);
        $('.org-name', clone2).attr('title', value.comp_name);
        $('.compliancedescription', clone2).text(value.descp);
        $('.applicablelocation', clone2).attr('id', 'appl' + sno);
        $('.applicablelocation', clone2).text(value.unit_wise_status.length + '/' + ACTIVE_UNITS.length);

       /* $('.saved', clone2).attr('id', 'save' + sno);
        if (value.comp_status > 0 && value.s_s == 1) {
            $('.saved', clone2).addClass('fa-square');
        }*/
        temp1 = temp1 + clone2.html();

        var unitRow = $('.mul-unit-head');
        var clone5 = unitRow.clone();
        $('tr', clone5).addClass('act' + count);
       
        temp1 = temp1 + clone5.html();
        sno++;
        var temp = "";
        var applUnits = value.unit_wise_status;
        $.each(applUnits, function(key1, value1) {
            var unitRow = $('.mul-unit-row');
            var clone4 = unitRow.clone();

            if (value1.is_new) {
                $('tr', clone4).addClass('act' + count + ' new_row');
            }else{
                $('tr', clone4).addClass('act' + count);
            }

            var combineId = value.comp_id + '#' + value1.unit_id + '#' + value1.c_comp_id + '#' + count;
            $('.combineid-class', clone4).attr('id', 'combineid' + statutoriesCount);
            $('.combineid-class', clone4).val(combineId);

            $('.unit-locatiion', clone4).text(UNIT_CS_ID[value1.unit_id].u_address);
            $('.unit-name', clone4).text(UNIT_CS_ID[value1.unit_id].u_name);

           
            if(value1.comp_app_status){
                $('.applicable', clone4).html('<img src="images/tick1bold.png">');
            }else{
                $('.applicable', clone4).html('<img src="images/deletebold.png">');
            }

            $('.opted', clone4).attr('id', 'comp' + statutoriesCount);
            $('.opted', clone4).val(statutoriesCount);
            $('.opted', clone4).addClass('comp' + count);

            
            if (value1.comp_opt_status) {
                $('.opted', clone4).html('<img src="images/tick-orange.png">').attr('for', '1');
            } else {
                $('.opted', clone4).html('<img src="images/deletebold.png">').attr('for', '2');
                /*$('#remark' + actCount).val(value.remarks);
                $('#r-view' + actCount).show();*/
            }

            $('.remarks').on('input', function(e) {
                this.value = isCommon($(this));
            });
    
            temp = temp + clone4.html();
            statutoriesCount++;

            if(value1.is_saved == false){
                var C_U_ID = value.comp_id + '-' + value1.unit_id;
                SELECTED_COMPLIANCE[C_U_ID] = {
                    'c_c_id': value1.c_comp_id,
                    'a_status': c_bool(value.opt_status),
                    'n_a_remarks': value.not_app_remarks,
                    'comp_id': value.comp_id,
                    'c_o_status': c_bool(value1.comp_opt_status),
                    'c_remarks': null,
                    'u_name': UNIT_CS_ID[value1.unit_id].u_name,
                    'u_id': value1.unit_id
                }
                console.log(SELECTED_COMPLIANCE);
            }

        });
        temp1 = temp1 + temp;
    });

    $('.tbody-assignstatutory').append(temp1);

    $( ".change_status" ).unbind( "click" );
    $('.change_status').click(function() {
        if ($(this).attr('for') == "1") {
            $(this).html('<img src="images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="images/tick1bold.png">').attr('for', '1');
        }
        mactstatus(this);
    });

    $( ".opted").unbind( "click" );
     $('.opted').on('click', function() {
        if ($(this).attr('for') == "1") {
            $(this).html('<img src="images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="images/tick-orange.png">').attr('for', '1');
        }
        mcompliancestatus(this);
    });

    $( ".remarks" ).unbind( "click" );
    $('.remarks').focusout(function() {
        mremarkstatus(this);
    });

    if (sno <= 0) {
        SubmitButton.hide();
        SaveButton.hide();
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
/*
function showList() {
    CURRENT_TAB = 1;
    StatutorySettingsView.show();
    StatutorySettingsAdd.hide();
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
                StatutorySettingsView.hide();
                StatutorySettingsAdd.show();
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
}*/

function loadEntityDetails(){
    if(LEGAL_ENTITIES.length > 1){
        BusinessGroupNameLabel.hide();
        BusinessGroupNameAC.show();
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();

        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        StatutorySettingsList.append(clone);
        SelectedUnitView.hide();
        EditButton.hide();

    }else{
        var BG_NAME = '-';
        if(LEGAL_ENTITIES[0]["bg_name"] != null){
            BG_NAME = LEGAL_ENTITIES[0]["bg_name"];
        }
        var BG_ID = '';
        if(LEGAL_ENTITIES[0]["bg_id"] != null){
            BG_ID = LEGAL_ENTITIES[0]["bg_id"];
        }

        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
        BusinessGroupNameLabel.show();
        BusinessGroupNameAC.hide();
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(LE_NAME);
        BusinessGroupNameLabel.text(BG_NAME);
        LegalEntityId.val(LE_ID);
        BusinessGroupId.val(BG_ID);
        Show.trigger( "click" );
    }

}

function initialize() {
    pageControls();
    callAPI(API_FILTERS);
    loadEntityDetails();
    //showList();
}

function showhide(ele) {
    var id = $(ele).attr('for');
    $('.act'+id).toggle();
}

$(function() {
    initialize();
    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
});
