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
var LastCompliance = '';
var statutoriesCount = 1;
var actCount = 1;
var count = 1;
var sno = 1;
var msno = 1;
var totalRecord = 0;
var mUnit = 20;
var OldApplLength = 0;

AssignStatutoryList.empty();
SingleAssignStatutoryList.empty();
var SELECTED_COMPLIANCE = {};
var ACT_MAP = {};
var isAuthenticate;
var C_COUNT = 0;

var L_DOMAIN = '';
var L_UNIT = '';
var L_STATUS = '';

var ListFilterBox = $('.js-filter');
var ListFilterUnit = $('#l-filter-unit');
var ListFilterLocation = $('#l-filter-location');
var ListFilterDomain = $('#l-filter-domain');
var ListFilterNoofComp = $('#l-filter-noofcompliance');
var ListFilterUpdBy = $('#l-filter-updatedby');
var ListFilterUpdOn = $('#l-filter-updatedon');

function callAPI(api_type) {
    if (api_type == API_FILTERS) {
        displayLoader();
        client_mirror.getStatutorySettingsFilters(function(error, data) {
            if (error == null) {
                DIVISIONS = data.div_infos;
                CATEGORIES = data.cat_info;
                //loadAssignedStatutories();
                hideLoader();
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
                displaySuccessMessage(message.statu_setting_unlock_success);
                //loadEntityDetails();
                Show.trigger( "click" );
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
        //check remark validation
        for(var i=1; i<=(actCount-1); i++){
            var aStatus = parseInt($('#act'+i).attr("for"));
            var remark = null;
            if(aStatus == 2 || aStatus==3){
                remark = $('#remark'+i).val().trim();
                if(remark==''){
                    displayMessage(message.act_remarks_opted_required);
                    hideLoader();
                    return false;
                }else if(isLengthMinMax($('#remark'+i), 1, 500, message.remark_should_not_exceed_500) == false){
                    hideLoader();
                    return false;
                }
            }
        }

        var selected_compliances_list = [];
        var remarks_flag = true;

        $.each(SELECTED_COMPLIANCE, function(key, value) {
            if( (value.c_o_status != value.c_a_status) && (value.c_remarks == null || value.c_remarks == '') && (value.n_a_remarks == null)){
                displayMessage(message.remarks_required);
                hideLoader();
                remarks_flag = false;
                return false;
            }else if( value.c_remarks != null && value.c_remarks.length > 500){
                displayMessage(message.remark_should_not_exceed_500);
                hideLoader();
                remarks_flag = false;
                return false;
            }else{
                selected_compliances_list.push(
                    value
                );
            }
        });

        if(remarks_flag){
            if (submission_status == 1) {
                client_mirror.saveStatutorySettings(selected_compliances_list, parseInt(LegalEntityId.val()), submission_status,
                    DOMAIN_ID, ACTIVE_UNITS,
                    function(error, data) {
                        if (error == null) {
                            displaySuccessMessage(message.statu_setting_save_success);
                            reset();
                            StatutorySettingsView.show();
                            StatutorySettingsAdd.hide();
                            Show.trigger( "click" );
                            //loadEntityDetails();
                            hideLoader();
                        } else {
                            if(error == 'InvalidPassword'){
                                displayMessage(message.invalid_password);
                            }else{
                                displayMessage(error);
                            }
                            hideLoader();
                        }
                    }
                );
            } else {
                client_mirror.updateStatutorySettings(CurrentPassword.val(), selected_compliances_list, parseInt(LegalEntityId.val()), submission_status,
                    DOMAIN_ID, ACTIVE_UNITS,
                    function(error, data) {
                        if (error == null) {
                            displaySuccessMessage(message.statu_setting_set_success);
                            reset();
                            StatutorySettingsView.show();
                            StatutorySettingsAdd.hide();
                            Show.trigger( "click" );
                            //loadEntityDetails();
                            hideLoader();
                        } else {
                            if(error == 'InvalidPassword'){
                                displayMessage(message.invalid_password);
                            }else{
                                displayMessage(error);
                            }
                            hideLoader();
                        }
                    }
                );
            }

        }
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
}

//validate
function validateAuthentication() {
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    }else if(isLengthMinMax($('#current-password'), 1, 20, message.password_should_not_exceed_20) == false){
        return false;
    } else {
        isAuthenticate = true;
        Custombox.close();
    }
    displayLoader();
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
            $(".tbody-statutorysettings-list .unit-checkbox").prop('checked', false);
            $('.tbody-statutorysettings-list .unit-checkbox').each(function(index, el) {
                if($(el).val() != 0){
                    if (SelectAll.prop('checked')) {
                        var chkid = $(el).val().split(',');
                        if(DOMAIN_ID == null || DOMAIN_ID == chkid[1]){
                            $(this).prop("checked", true);
                            DOMAIN_ID = parseInt(chkid[1]);

                            ACTIVE_UNITS.push(parseInt(chkid[0]));
                            C_COUNT = C_COUNT + parseInt(chkid[2]);

                            if(C_COUNT > 5000){
                                displayMessage(message.maximum_compliance_selection_reached_select_all);
                                return false;
                            }
                            else if (ACTIVE_UNITS.length >= mUnit) {
                                displayMessage(message.maximum_units);
                                return false;
                            } else {
                                return true;
                            }

                        }else{
                            $(this).prop("checked", false);
                        }
                    } else {
                        DOMAIN_ID = null;
                        $(this).prop("checked", false);
                    }
                }
            });
            SelectedUnitCount.text(ACTIVE_UNITS.length);
        }
    });

    EditButton.click(function() {
        //reset();
        if(ACTIVE_UNITS.length > 0){
            sno = 1;
            msno = 1;
            statutoriesCount = 1;
            $(".total_count_view").hide();
            $('.tbody-compliance-list').empty();
            ShowMore.hide();
            SaveButton.hide();
            SubmitButton.hide();
            StatutorySettingsView.hide();
            StatutorySettingsAdd.show();
            callAPI(API_Wizard1);
        }else{
            displayMessage(message.atleast_one_unit_required);
        }

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
            var condition_fields = ["le_id"];
            var condition_values = [LegalEntityId.val()];
            if (BusinessGroupId.val() != '') {
                condition_fields.push("bg_id");
                condition_values.push(BusinessGroupId.val());
            }
            if (DivisionId.val() != '') {
                condition_fields.push("div_id");
                condition_values.push(DivisionId.val());
            }
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACCategory, CategoryId, text_val,
                CATEGORIES, "cat_name", "cat_id",
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
        //displayPopUp(SAVE_API, null);
        displayLoader();
        setTimeout(function() {
            callAPI(SAVE_API)
        }, 500);
    });

    PasswordSubmitButton.click(function() {
        validateAuthentication();
    });

    ListFilterBox.keyup(function() {
        processListFilter();
    });
}


function reset() {
    sno = 1;
    msno = 1;
    statutoriesCount = 1;
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
                    loadUnits(UNITS);
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
        });
    }
}

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

        if(DOMAIN_ID == null || DOMAIN_ID == chkid[1]){
            
            if(C_COUNT > 5000){
                displayMessage(message.maximum_compliance_selection_reached_select_all);
                $(element).prop("checked", false);
                return false;
            }
            else if (ACTIVE_UNITS.length >= mUnit) {
                displayMessage(message.maximum_units);
                $(element).prop("checked", false);
                return false;
            }else{
                $(element).prop("checked", true);
                DOMAIN_ID = parseInt(chkid[1]);
                ACTIVE_UNITS.push(parseInt(chkid[0]));
                C_COUNT = C_COUNT + parseInt(chkid[2]);
                SelectedUnitCount.text(ACTIVE_UNITS.length);
                return true;
            }

        }else{
            $(element).prop("checked", false);
            displayMessage(message.unit_selection_should_be_same_domain);
        }


    } else {
        index = ACTIVE_UNITS.indexOf(parseInt(chkid[0]));
        ACTIVE_UNITS.splice(index, 1);
        C_COUNT = C_COUNT - parseInt(chkid[2]);
    }
    if(ACTIVE_UNITS.length == 0){
        SelectAll.prop('checked', false);
        DOMAIN_ID = null;
    }
    SelectedUnitCount.text(ACTIVE_UNITS.length);
}

function loadUnits(F_UNITS) {
    ACTIVE_UNITS = [];
    SelectedUnitCount.text(ACTIVE_UNITS.length);
    SelectAll.prop("checked", false);
    DOMAIN_ID = null;

    C_COUNT = 0;
    UNIT_CS_ID = {};
    StatutorySettingsList.empty();
    $.each(F_UNITS, function(key, value) {
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

        if(value.is_locked){
            $('.ck-view', clone).hide();
            $('.unit-checkbox', clone).attr('id', 'unit' + key);
            $('.unit-checkbox', clone).val(0);

        }else{
            $('.ck-view', clone).show();
            $('.unit-checkbox', clone).attr('id', 'unit' + key);
            $('.unit-checkbox', clone).val(value.u_id + ',' + value.d_id + ',' + value.r_count);
        }

        $('.tbl_unit', clone).text(value.u_name);
        $('.tbl_address', clone).attr('title', value.address);

        var location = value.location.replace(/ >>/gi, ',');
        $('.tbl_location', clone).text(location);
        $('.tbl_domain', clone).text(value.d_name);
        $('.tbl_no_of_compliance', clone).text(value.r_count);
        $('.tbl_updated_by', clone).text(upd_by);
        $('.tbl_updated_on', clone).text(upd_on);
        if(value.is_locked){
            $('.tbl_lock', clone).addClass('fa-lock');
            if(value.allow_unlock == true){
                $('.tbl_lock', clone).attr('title', 'Click here to Unlock');
            }
        }else{
            $('.tbl_lock', clone).addClass('fa-unlock');
            //$('.tbl_lock', clone).find('i').attr('title', 'Click here to Lock');
        }

        $('.tbl_lock', clone).click(function() {
            if(value.is_locked){
                if(value.allow_unlock == true){
                    //displayLockPopUp(value.u_id);
                    displayPopUp(LOCK_API, [value.u_id, value.d_id, value.is_locked]);
                }else{
                    displayMessage(message.unlock_permission);
                }
            }
        });

        $('.unit-checkbox', clone).on('click', function(e) {
            activateUnit(this);
        });

        StatutorySettingsList.append(clone);

        UNIT_CS_ID[value.u_id] = {
            'u_name': value.u_name,
            'u_address': location
        }

    });

    if(UNITS == null || UNITS.length == 0){
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

        var C_A_STATUS = true;
        if($(this).attr("data-applicable") == 'false') C_A_STATUS = false;

        var C_REMARK = $(this).attr("data-remark");

        if (checkedVal > 1) {
            $(this).html('<img src="/images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="/images/tick-orange.png">').attr('for', '1');
        }
        var sid = $(this).val();
        $('#save' + sid).addClass('fa-square');

        var C_A_STATUS1 = 1;
        if($(this).attr("data-applicable") == 'false') C_A_STATUS1 = 2;

        if(checkedVal == 1 && checkedVal != C_A_STATUS1){
            $('#c-remark-input-' + sid).val(C_REMARK)
            $('#c-remark-add-' + sid).show();
            $('#c-remark-view-' + sid).hide();
        }else{
            $('#c-remark-add-' + sid).hide();
            $('#c-remark-view-' + sid).hide();
        }

        var combine_ids = $('#combineid' + sid).val().split('#');
        SELECTED_COMPLIANCE[combine_ids[0]] = {
            'c_c_id': parseInt(combine_ids[2]),
            'a_status': c_bool(checkedVal),
            'n_a_remarks': A_REMARK,
            'comp_id': parseInt(combine_ids[0]),
            'c_o_status': c_bool(checkedVal),
            'c_remarks': C_REMARK,
            'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
            'u_id': parseInt(combine_ids[1]),
            'c_a_status': C_A_STATUS
        }
        //console.log(SELECTED_COMPLIANCE)
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
        var C_A_STATUS = true;
        if($(this).attr("data-applicable") == 'false') C_A_STATUS = false;

        var sid = $(this).val();
        var combine_ids = $('#combineid' + sid).val().split('#');

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
                'u_id': parseInt(combine_ids[1]),
                'c_a_status': C_A_STATUS
            }
        }
    });
    //console.log(SELECTED_COMPLIANCE);
}

function cremarkstatus(element) {
    var ID = $(element).attr("id").split('-').pop();

    //if($(element).val() != ''){
    var C_REMARK = $(element).val();
    var combine_ids = $('#combineid' + ID).val().split('#');
    SELECTED_COMPLIANCE[combine_ids[0]].c_remarks = C_REMARK;
    //}
    //console.log(SELECTED_COMPLIANCE);
}

function compliancestatus(element, C_ID, U_ID, A_ID) {

    var sid = $(element).val();
    $('#save' + sid).addClass('fa-square');

    var combine_ids = $('#combineid' + sid).val().split('#');
    var A_STATUS = $('#act' + combine_ids[3]).attr("for");
    var A_REMARK = null;

    var C_STATUS = parseInt($(element).attr("for"));
    var C_A_STATUS = true;
    if($(element).attr("data-applicable") == 'false') C_A_STATUS = false;

    var C_REMARK = $(element).attr("data-remark");

    //alert(c_bool(C_STATUS) + '!=' + C_A_STATUS)
    if(c_bool(C_STATUS) != C_A_STATUS){
        $('#c-remark-input-' + sid).val(C_REMARK)
        $('#c-remark-add-' + sid).show();
        $('#c-remark-view-' + sid).hide();
    }else{
        $('#c-remark-add-' + sid).hide();
        $('#c-remark-view-' + sid).hide();
        C_REMARK = null;
    }

    /*alert( C_A_STATUS + '==' + c_bool(C_STATUS))*/
    if (C_STATUS > 1 && $('#remark' + combine_ids[3]).val() != '') {
        A_REMARK = $('#remark' + combine_ids[3]).val();
    }
    SELECTED_COMPLIANCE[combine_ids[0]] = {
        'c_c_id': parseInt(combine_ids[2]),
        'a_status': c_bool(A_STATUS),
        'n_a_remarks': A_REMARK,
        'comp_id': parseInt(combine_ids[0]),
        'c_o_status': c_bool(C_STATUS),
        'c_remarks': C_REMARK,
        'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
        'u_id': parseInt(combine_ids[1]),
        'c_a_status': C_A_STATUS
    }

    var actSelect = combine_ids[3];
    var cStatus = false;
    var checkedVal = 2;
    $('.comp' + actSelect).each(function () {
        if($(this).attr("for") == 1){
            cStatus = true;
            checkedVal = 1;
        }
    });

    var old_a_status = parseInt($('#act'+actSelect).attr("for"));
    if(old_a_status != checkedVal){
            if (cStatus) {
            $('#act' + actSelect).html('<img src="/images/tick1bold.png">').attr('for', '1');
           
            $('#r-view' + actSelect).hide();
            $('.comp' + actSelect).each(function () {
                var sid1 = $(this).val();
                var C_A_STATUS1 = 1;
                if($(this).attr("data-applicable") == 'false') C_A_STATUS1 = 2;

                var C_STATUS1 = parseInt($(this).attr("for"));
                //alert(C_STATUS1 + '!=' + C_A_STATUS1)
                //alert(checkedVal)

                var C_A_STATUS = true;
                if($(this).attr("data-applicable") == 'false') C_A_STATUS = false;
                var C_REMARK = $(this).attr("data-remark");

                if(checkedVal == 1 && C_STATUS1 != C_A_STATUS1){
                    $('#c-remark-input-' + sid1).val(C_REMARK)
                    $('#c-remark-add-' + sid1).show();
                    $('#c-remark-view-' + sid1).hide();
                }else{
                    $('#c-remark-add-' + sid1).hide();
                    $('#c-remark-view-' + sid1).hide();
                    C_REMARK = null;
                }

                var combine_ids = $('#combineid' + sid1).val().split('#');
                SELECTED_COMPLIANCE[combine_ids[0]] = {
                    'c_c_id': parseInt(combine_ids[2]),
                    'a_status': c_bool(checkedVal),
                    'n_a_remarks': A_REMARK,
                    'comp_id': parseInt(combine_ids[0]),
                    'c_o_status': c_bool(C_STATUS1),
                    'c_remarks': C_REMARK,
                    'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
                    'u_id': parseInt(combine_ids[1]),
                    'c_a_status': C_A_STATUS
                }
            });
        } else {
            $('#act' + actSelect).html('<img src="/images/deletebold.png">').attr('for', '2');
            $('#remark' + actSelect).show();
            $('#r-view' + actSelect).show();
            $('.comp' + actSelect).each(function () {
                var sid1 = $(this).val();
                $('#c-remark-add-' + sid1).hide();
                $('#c-remark-view-' + sid1).hide();

                var C_A_STATUS = false;
                var C_REMARK = null;

                var combine_ids = $('#combineid' + sid1).val().split('#');
                SELECTED_COMPLIANCE[combine_ids[0]] = {
                    'c_c_id': parseInt(combine_ids[2]),
                    'a_status': c_bool(checkedVal),
                    'n_a_remarks': A_REMARK,
                    'comp_id': parseInt(combine_ids[0]),
                    'c_o_status': c_bool(checkedVal),
                    'c_remarks': C_REMARK,
                    'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
                    'u_id': parseInt(combine_ids[1]),
                    'c_a_status': C_A_STATUS
                }
            });
        }
    }
    //console.log(SELECTED_COMPLIANCE);
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

        if (checkedVal > 1) {
            $(this).html('<img src="/images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="/images/tick-orange.png">').attr('for', '1');
        }

        var sname = $(this).attr('id');
        var sid = sname.substr(sname.lastIndexOf('p') + 1);
        $('#save' + sid).addClass('fa-square');

        var C_REMARK = $(this).attr("data-remark");
        var C_A_STATUS = 1;
        if($(this).attr("data-applicable") == 'false') C_A_STATUS = 2;

        if(checkedVal == 1 && checkedVal != C_A_STATUS){
            $('#c-remark-add-' + sid).show();
            $('#c-remark-view-' + sid).hide();
        }else{
            $('#c-remark-add-' + sid).hide();
            $('#c-remark-view-' + sid).hide();
        }

        C_A_STATUS = true;
        if($(element).attr("data-applicable") == 'false') C_A_STATUS = false;

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
            'c_remarks': C_REMARK,
            'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
            'u_id': parseInt(combine_ids[1]),
            'c_a_status': C_A_STATUS
        }
    });
    //console.log(SELECTED_COMPLIANCE)
}

function mcompliancestatus(element) {
    var C_S_ID = null;
    /*var sname = $(element).attr('class');
    var sid = sname.substr(sname.lastIndexOf('-') + 1);
    $('#save' + sid).addClass('fa-square');*/

    var sname1 = $(element).attr('id');
    var sid1 = sname1.substr(sname1.lastIndexOf('p') + 1);

    $('#save' + sid1).addClass('fa-square');

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

    var C_A_STATUS = true;
    if($(element).attr("data-applicable") == 'false') C_A_STATUS = false;

    var C_REMARK = $(element).attr("data-remark");
    if(c_bool(C_STATUS) != C_A_STATUS){
        $('#c-remark-add-' + sid1).show();
        $('#c-remark-view-' + sid1).hide();
    }else{
        $('#c-remark-add-' + sid1).hide();
        $('#c-remark-view-' + sid1).hide();
        C_REMARK = null;
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
        'c_remarks': C_REMARK,
        'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
        'u_id': parseInt(combine_ids[1]),
        'c_a_status': C_A_STATUS
    }
    //console.log(SELECTED_COMPLIANCE);
}

function mcremarkstatus(element) {
    var ID = $(element).attr("id").split('-').pop();

    if($(element).val() != ''){
        var C_REMARK = $(element).val();
        var combine_ids = $('#combineid' + ID).val().split('#');
        var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
        SELECTED_COMPLIANCE[C_U_ID].c_remarks = C_REMARK;
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

    var currentAction = '.comp' + ID;
    $(currentAction).each(function() {
        var C_A_STATUS = true;
        if($(this).attr("data-applicable") == 'false') C_A_STATUS = false;

        var sname = $(this).attr("id");
        var sid = sname.substr(sname.lastIndexOf('p') + 1);

        var combine_ids = $('#combineid' + sid).val().split('#');

        var C_STATUS = parseInt($(this).attr("for"));

        if (C_STATUS > 1) {
            var C_U_ID = combine_ids[0] + '-' + combine_ids[1];
            SELECTED_COMPLIANCE[C_U_ID] = {
                'c_c_id': parseInt(combine_ids[2]),
                'a_status': c_bool(A_STATUS),
                'n_a_remarks': A_REMARK,
                'comp_id': parseInt(combine_ids[0]),
                'c_o_status': c_bool(C_STATUS),
                'c_remarks': null,
                'u_name': UNIT_CS_ID[combine_ids[1]].u_name,
                'u_id': parseInt(combine_ids[1]),
                'c_a_status': C_A_STATUS
            }
        }
    });
    //console.log(SELECTED_COMPLIANCE);
}

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
                $('#act' + actCount).html('<img src="/images/tick1bold.png">').attr('for', '1');
            } else {
                $('#act' + actCount).html('<img src="/images/deletebold.png">').attr('for', '2');
                $('#remark' + actCount).val(value.not_app_remarks);
                $('#r-view' + actCount).show();
            }

            $('#act' + actCount).click(function() {
                if ($(this).attr('for') == "1") {
                    $(this).html('<img src="/images/deletebold.png">').attr('for', '2');
                } else {
                    $(this).html('<img src="/images/tick1bold.png">').attr('for', '1');
                }
                actstatus(this);
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
            $('.compliancefrequency', clone2).text(value.frequency_name);
            $('.compliancedescription', clone2).text(value.descp);

            if(value1.comp_app_status){
                $('.applicable', clone2).html('<img src="/images/tick1bold.png">');
            }else{
                $('.applicable', clone2).html('<img src="/images/deletebold.png">');
            }

            var c_r = '';
            if(value1.comp_remarks != null) c_r = value1.comp_remarks;

            $('.opted', clone2).attr("data-remark", c_r);
            $('.opted', clone2).attr("data-applicable", value1.comp_app_status);
            $('.opted', clone2).attr('id', 'comp' + statutoriesCount);
            $('.opted', clone2).val(statutoriesCount);
            $('.opted', clone2).addClass('comp' + count);

            $('.c-remark-view', clone2).attr('id', 'c-remark-view-' + statutoriesCount);
            $('.c-remark-add', clone2).attr('id', 'c-remark-add-' + statutoriesCount);
            $('.c-remark-input', clone2).attr('id', 'c-remark-input-' + statutoriesCount);

            if(value1.comp_remarks != null){
                $('.c-remark-view i', clone2).attr('title', value1.comp_remarks);
                $('.c-remark-view span', clone2).text(part_compliance(value1.comp_remarks));
            }else{
                $('.c-remark-view', clone2).hide();
                /*if(value1.comp_app_status != value1.comp_opt_status && value.opt_status){
                    $('.c-remark-add', clone2).show();
                }*/
            }
            $('.saved', clone2).attr('id', 'save' + statutoriesCount);
            if (value1.is_saved) {
                $('.saved', clone2).addClass('fa-square');
            }

            $('.opted', clone2).on('click', function() {
                if ($(this).attr('for') == "1") {
                    $(this).html('<img src="/images/deletebold.png">').attr('for', '2');
                } else {
                    $(this).html('<img src="/images/tick-orange.png">').attr('for', '1');
                }
                compliancestatus(this, value.comp_id, value.u_id, value.level_1_s_id);
            });


            $('#collapse' + count + ' .tbody-compliance-list').append(clone2);

            $('#c-remark-input-' + statutoriesCount).focusout(function() {
                cremarkstatus(this);
            });

            $('.c-remark-input').on('input', function(e) {
                this.value = isCommon($(this));
            });

            if (value1.comp_opt_status) {
                $('#comp' + statutoriesCount).html('<img src="/images/tick-orange.png">').attr('for', '1');
            } else {
                $('#comp' + statutoriesCount).html('<img src="/images/deletebold.png">').attr('for', '2');
                /*$('#remark' + actCount).val(value.remarks);
                $('#r-view' + actCount).show();*/
            }

            /*$('#comp' + statutoriesCount).click(function() {
                if ($(this).attr('for') == "1") {
                    $(this).html('<img src="/images/deletebold.png">').attr('for', '2');
                } else {
                    $(this).html('<img src="/images/tick-orange.png">').attr('for', '1');
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
                    'c_remarks': value1.comp_remarks,
                    'u_name': UNIT_CS_ID[value1.unit_id].u_name,
                    'u_id': value1.unit_id,
                    'c_a_status': value1.comp_app_status
                }
                //console.log(SELECTED_COMPLIANCE);
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
    var isNew = true;
    $.each(COMPLIANCES_LIST, function(key, value) {
        if (LastAct != value.lone_statu_name) {
            var actHeadingRow = $('.mul-act-heading');
            var clone = actHeadingRow.clone();
            $('.panel-title span', clone).text(value.lone_statu_name);
            $('.change_status', clone).attr('id', 'act' + actCount);
            $('.change_status', clone).attr("data-act", actCount);
            $('.toggle-act', clone).closest("div").attr('for', actCount);

            $('.r-view', clone).attr('id', 'r-view' + actCount);
            $('.remarks', clone).attr('id', 'remark' + actCount);
            $('.remarks', clone).attr("data-act", actCount);

            if (value.opt_status) {
                $('.change_status', clone).html('<img src="/images/tick1bold.png">').attr('for', '1');
            } else {
                $('.change_status', clone).html('<img src="/images/deletebold.png">').attr('for', '2');
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
            LastCompliance = "";
            OldApplLength = 0;
        }

        var applUnits = value.unit_wise_status;
        var applcount = 0;
        if(isNew && LastCompliance == value.comp_id){
            applcount = applUnits.length + OldApplLength;
            $('#appl'+(msno - 1)).text(applcount + '/' + ACTIVE_UNITS.length);
        }
        isNew = false;

        if(LastCompliance != value.comp_id){
            var complianceDetailtableRow = $('.mul-compliance-details');
            var clone2 = complianceDetailtableRow.clone();
            applcount = applUnits.length;

            $('tr', clone2).addClass('act' + count);
            $('.sno', clone2).text(msno);
            $('.statutoryprovision', clone2).text(value.s_prov);
            $('.compliancetask', clone2).text(value.comp_name);
            $('.compliancefrequency', clone2).text(value.frequency_name);
            $('.compliancedescription', clone2).text(value.descp);
            $('.applicablelocation', clone2).attr('id', 'appl' + msno);
            $('.applicablelocation', clone2).text(applcount + '/' + ACTIVE_UNITS.length);
           /* $('.saved', clone2).attr('id', 'save' + sno);
            if (value.comp_status > 0 && value.s_s == 1) {
                $('.saved', clone2).addClass('fa-square');
            }*/
            temp1 = temp1 + clone2.html();

            var unitRow = $('.mul-unit-head');
            var clone5 = unitRow.clone();
            $('tr', clone5).addClass('act' + count);
            temp1 = temp1 + clone5.html();
            msno++;
            LastCompliance = value.comp_id;
            OldApplLength = applUnits.length;
        }

        var temp = "";
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
                $('.applicable', clone4).html('<img src="/images/tick1bold.png">');
            }else{
                $('.applicable', clone4).html('<img src="/images/deletebold.png">');
            }

            var c_r = '';
            if(value1.comp_remarks != null) c_r = value1.comp_remarks;
            $('.opted', clone4).attr("data-remark", c_r);
            $('.opted', clone4).attr("data-applicable", value1.comp_app_status);
            $('.opted', clone4).attr('id', 'comp' + statutoriesCount);
            $('.opted', clone4).val(statutoriesCount);
            $('.opted', clone4).addClass('comp' + count);

            $('.c-remark-view', clone4).attr('id', 'c-remark-view-' + statutoriesCount);
            $('.c-remark-add', clone4).attr('id', 'c-remark-add-' + statutoriesCount);
            $('.c-remark-input', clone4).attr('id', 'c-remark-input-' + statutoriesCount);

            if(value1.comp_remarks != null){
                $('.c-remark-view i', clone4).attr('title', value1.comp_remarks);
                $('.c-remark-view span', clone4).text(part_compliance(value1.comp_remarks));
            }else{
                $('.c-remark-view', clone4).hide();
            }

            if (value1.comp_opt_status) {
                $('.opted', clone4).html('<img src="/images/tick-orange.png">').attr('for', '1');
            } else {
                $('.opted', clone4).html('<img src="/images/deletebold.png">').attr('for', '2');
                /*$('#remark' + actCount).val(value.remarks);
                $('#r-view' + actCount).show();*/
            }

            $('.saved', clone4).attr('id', 'save' + statutoriesCount);
            if (value1.is_saved) {
                $('.saved', clone4).addClass('fa-square');
            }

            $('.remarks').on('input', function(e) {
                this.value = isCommon($(this));
            });

            temp = temp + clone4.html();
            statutoriesCount++;
            sno++;

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
                //console.log(SELECTED_COMPLIANCE);
            }

        });
        temp1 = temp1 + temp;
    });

    $('.tbody-assignstatutory').append(temp1);

    $( ".change_status" ).unbind( "click" );
    $('.change_status').click(function() {
        if ($(this).attr('for') == "1") {
            $(this).html('<img src="/images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="/images/tick1bold.png">').attr('for', '1');
        }
        mactstatus(this);
        return false;
    });

    $( ".opted").unbind( "click" );
     $('.opted').on('click', function() {
        if ($(this).attr('for') == "1") {
            $(this).html('<img src="/images/deletebold.png">').attr('for', '2');
        } else {
            $(this).html('<img src="/images/tick-orange.png">').attr('for', '1');
        }
        mcompliancestatus(this);
    });

    $( ".remarks" ).unbind( "click" );
    $('.remarks').focusout(function() {
        mremarkstatus(this);
    });

    $('.c-remark-input').focusout(function() {
        mcremarkstatus(this);
    });

    if (msno <= 0) {
        SubmitButton.hide();
        SaveButton.hide();
        $(".total_count_view").hide();
    } else {
        SaveButton.show();
        if (C_COUNT == (sno - 1)) {
            SubmitButton.show();
            ShowMore.hide();
        } else {
            SubmitButton.hide();
            ShowMore.show();
        }
        $(".total_count").text('Showing 1 to ' + (msno - 1) + ' of ' + totalRecord + ' entries');
        $(".total_count_view").show();
    }
    hideLoader();
}

function processListFilter() {
    var unitfilter = ListFilterUnit.val().toLowerCase();
    var locationfilter = ListFilterLocation.val().toLowerCase();
    var domainfilter = ListFilterDomain.val().toLowerCase();
    var noofcompliancefilter = ListFilterNoofComp.val().toLowerCase();
    var updbyfilter = ListFilterUpdBy.val().toLowerCase();
    var updonfilter = ListFilterUpdOn.val().toLowerCase();
    var filteredList = [];
    for (var entity in UNITS) {
        var u_name = UNITS[entity].u_name;
        var location = UNITS[entity].location.replace(/ >>/gi, ',');
        var domain = UNITS[entity].d_name;
        var noofcomp = UNITS[entity].r_count.toString();

        var upd_by = '-';
        if(UNITS[entity].usr_by != null){
            upd_by = UNITS[entity].usr_by;
        }
        var upd_on = '-';
        if(UNITS[entity].usr_on != null){
            upd_on = UNITS[entity].usr_on;
        }

        if (~u_name.toLowerCase().indexOf(unitfilter) && ~location.toLowerCase().indexOf(locationfilter)
            && ~domain.toLowerCase().indexOf(domainfilter) && ~noofcomp.indexOf(noofcompliancefilter)
            && ~upd_by.toLowerCase().indexOf(updbyfilter) && ~upd_on.toLowerCase().indexOf(updonfilter)) {
            filteredList.push(UNITS[entity]);
        }
    }
    loadUnits(filteredList);
}

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
    /*$(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });*/
});
