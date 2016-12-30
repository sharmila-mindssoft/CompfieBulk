/* Elements */
var UserType = $("#usertype");
var Show = $(".btn-show");


// Group auto complete
var GroupDiv = $(".filter-group-div");


// Entity auto complete
var EntityDiv = $(".filter-legal-div");
var EntityName = $("#legal_entity_name");
var EntityId = $("#legal_entity_id");
var ACEntity = $("#ac-entity")

// Techno manager autocomplete
var TechnoManagerDiv = $(".techno-mgr-div");
var RTTechnoManagerName = $("#rt_techno_manager_name");
var RTTechnoManagerId = $("#rt_techno_manager_id");
var ACRTTechnoManager = $("#ac-rt-techno-manager");

// Techno User autocomplete
var TechnoUserDiv = $(".techno-user-div");

var RTTechnoUserName = $("#rt_techno_user_name");
var RTTechnoUserId = $("#rt_techno_user_id");
var ACRTTechnoUser = $("#ac-rt-techno-user");

// Domain manager autocomplete
var DomainManagerDiv = $(".domain-mgr-div");

var RTDomainManagerName = $("#rt_domain_manager_name");
var RTDomainManagerId = $("#rt_domain_manager_id");
var ACRTDomainManager = $("#ac-rt-domain-manager");

// Domain Executive autocomplete
var DomainUserDiv = $(".domain-user-div");
var DomainExecutiveName = $("#domain_executive_name");
var DomainExecutiveId = $("#domain_executive_id");
var ACDomainExecutive = $("#ac-domain-executive");
var RTDomainExecutiveName = $("#rt_domain_user_name");
var RTDomainExecutiveId = $("#rt_domain_user_id");
var ACRTDomainExecutive = $("#ac-rt-domain-user");

// Business Group auto complete
var BusinessGroupDiv = $(".filter-business-div");


// Domain auto complete
var DomainDiv = $(".filter-domain-div");


// Group View List
var GroupView = $(".group-view");
var TBodyReassignListGroupView = $(".tbody-reassign-list-group-view");
var GroupViewRow = $(".group-view-row tr");
var CountryNames = ".countries";
var Group_Name = ".group-name";
var LECount = ".le-count";
var GroupCheckBox = ".group-checkbox";

// Legal Entity View List
var LegalEntityView = $(".legalentity-view");
var TBodyReassignListLegalEntityView = $(".tbody-reassign-list-legalentity-view");
var LegalEntityViewRow = $(".legalentity-view-row tr")
var BG_Name = ".bg-name";
var Country = ".country";
var Entity = ".entity";
var EntityCheckBox = ".entity-checkbox";

// Unit view List
var UnitView = $(".unit-view");
var TBodyReassignListUnitView = $(".tbody-reassign-list-unit-view");
var UnitViewRow = $(".unit-view-row tr");
var UnitCode = ".unit-code";
var UnitName = ".unit-name";
var UnitLocation = ".location";
var UnitCheckBox  = ".unit-checkbox";


var ReassignToTechnoManager = $(".reassign-tm");
var ReassignToTechnoUser = $(".reassign-tu");
var ReassignToDomainManager = $(".reassign-dm");
var ReassignToDomainUser = $(".reassign-du");
var RemarksDiv = $(".remarks-div");
var Remarks = $(".remarks");
var ViewNote = $(".view-note");

var UnitHeaderCheckBox = $(".unit-header-checkbox");
var EntityHeaderCheckBox = $(".entity-header-checkbox");
var GroupHeaderCheckBox = $(".group-header-checkbox");



/* Variables */
var val_user_type = '';
var val_techno_manager_id = '';
var val_techno_executive_id = '';
var val_domain_manager_id = '';
var val_domain_executive_id = '';
var val_group_id = ''
var val_business_group_id = '';
var val_legal_entity_id = '';
var val_domain_id = '';

var TECHNO_MANAGERS = '';
var TECHNO_USERS = '';
var DOMAIN_MANAGERS = '';
var DOMAIN_USERS = '';
var GROUPS = '';
var BUSINESS_GROUPS = '';
var LEGAL_ENTITIES = '';
var UNITS = '';
var COUNTRIES = '';
var DOMAINS = '';
var ASSIGNED_ENTITIES = '';
var ASSIGNED_UNITS = '';
var ASSIGNED_CLIENTS = '';
var USER_CATEGORIES = '';
var client_id_name_map = {};
var country_id_name_map = {};
var business_group_id_name_map = {};
var user_wise_entities = {};
var user_wise_units = {};
var user_wise_clients = {};

var GroupCheckBoxes = {};
var EntityCheckBoxes = {};
var UnitCheckBoxes = {};


var selected_textbox = '';
var selected_textid = '';

var TechnoManagerName = $("#techno_manager_name");
var TechnoManagerId = $("#techno_manager_id");
var ACTechnoManager = $("#ac-techno-manager");
var TMShow = $(".tm-show-btn");
var Submit = $(".btn-submit-1");
var TechnoDetailsList = '';
var TMRemarks = $("#tm_remarks");
var TERemarks = $("#te_remarks");

var TEShow = $(".te-show-btn");
var TESubmit = $(".btn-submit-2");

var TechnoExecutiveName = $("#techno_executive_name");
var TechnoExecutiveId = $("#techno_executive_id");
var ACTechnoExecutive = $("#ac-techno-executive");

var RTechnoExecutiveName = $("#te-techno_executive_name");
var RTechnoExecutiveId = $("#te-techno_executive_id");
var RACTechnoExecutive = $("#te-ac-techno-executive");

var DomainManagerName = $("#domain_manager_name");
var DomainManagerId = $("#domain_manager_id");
var ACDomainManager = $("#ac-domain-manager");

var DMGroupName = $("#dm_group_name");
var DMGroupId = $("#dm_group_id");
var DMACGroup = $("#ac-dm-group");

var DMBusinessGroupName = $("#dm_business_group_name");
var DMBusinessGroupId = $("#dm_business_group_id");
var DMACBusinessGroup = $("#ac-dm-business-group");

var DMLegalEntityName = $("#dm_legal_entity_name");
var DMLegalEntityId = $("#dm_legal_entity_id");
var DMACLegalEntity = $("#ac-dm-legal-entity");

var DMDomainName = $("#dm_domain_name");
var DMDomainId = $("#dm_domain_id");
var DMACDomain = $("#ac-dm-domain");

var DMShow = $(".dm-show-btn");
var DMSubmit = $(".btn-submit-3");

var DomainDetailsList = '';

//retrive businessgroup form autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
}

function usertypeselectionlist(){
    user_type = UserType.val();
    clearGrids();
    if(user_type == 5){ // Techno Manager
        TechnoManagerDiv.show();
        TechnoUserDiv.hide();
        DomainManagerDiv.hide();
        GroupDiv.hide();
        BusinessGroupDiv.hide();
        EntityDiv.hide();
        DomainDiv.hide();
        DomainUserDiv.hide();
    }else if(user_type == 6){ // Techno User
        TechnoManagerDiv.hide();
        TechnoUserDiv.show();
        DomainManagerDiv.hide();
        GroupDiv.hide();
        BusinessGroupDiv.hide();
        EntityDiv.hide();
        DomainDiv.hide();
        DomainUserDiv.hide();
    }else if(user_type == 7){ // Domain Manager
        TechnoManagerDiv.hide();
        TechnoUserDiv.hide();
        DomainManagerDiv.show();
        GroupDiv.show();
        BusinessGroupDiv.show();
        EntityDiv.show();
        DomainDiv.show();
        DomainUserDiv.hide();
    }else if(user_type == 8){ // Domain User
        TechnoManagerDiv.hide();
        TechnoUserDiv.hide();
        DomainManagerDiv.hide();
        GroupDiv.show();
        BusinessGroupDiv.show();
        EntityDiv.show();
        DomainDiv.show();
        DomainUserDiv.show();
    }
}


function loadTMList(){
        var LastGroup = '';
        var group_countries = {};
        var group_domains = {};

        $.each(TechnoDetailsList, function(key, value) {
            if(LastGroup != value.ct_name){


                var grouptableRow = $('#templates .tm-view-row .tm-view-group-row');
                var clone = grouptableRow.clone();

                $('.tm-group-checkbox', clone).val(value.ct_id);
                $('.tm-group', clone).text(value.ct_name);
                $('.tm-ac-view', clone).addClass('tm-ac-'+value.ct_id);

                $('.tm-techno-manager-name', clone).attr('id', 'techno_manager_name_'+value.ct_id);
                $('.techno_manager_id', clone).attr('id', 'techno_manager_id_'+value.ct_id);
                $('.ac-techno-manager', clone).attr('id', 'ac-techno-manager-'+value.ct_id);

                $('.tm-techno-manager-name', clone).keyup(function(e){
                    var condition_fields = ["country_domains"];
                    var condition_values1 = [group_countries[value.ct_id]];
                    var condition_values2 = group_domains[value.ct_id];

                    var text_val = $(this).val();
                    selected_textbox = $(this);
                    selected_textid = $("#techno_manager_id_"+value.ct_id);

                    commonAutoComplete1(
                        e, $("#ac-techno-manager-"+value.ct_id), $("#techno_manager_id_"+value.ct_id), text_val,
                        TECHNO_MANAGERS, "employee_name", "user_id",  function (val) {
                            onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                        }, condition_fields, condition_values1, condition_values2);
                });

                $('.tbody-tm-view').append(clone);
                LastGroup = value.ct_name;

                group_countries[value.ct_id] = [];
                group_domains[value.ct_id] = [];
            }

            group_countries[value.ct_id] = group_countries[value.ct_id].push(value.c_id);
            group_domains[value.ct_id] = $.merge(group_domains[value.ct_id], value.d_ids);

            var letableRow = $('#templates .tm-view-row .tm-view-le-row');
            var clone = letableRow.clone();
            $('.tm-country', clone).text(value.c_name);
            $('.tm-le', clone).text(value.le_name);
            $('.te-ac-view', clone).addClass('te-ac-'+value.ct_id);

            $('.tm-techno-executive-name', clone).attr('id', 'techno_executive_name_'+value.le_id);
            $('.techno_executive_id', clone).attr('id', 'techno_executive_id_'+value.le_id);
            $('.ac-techno-executive', clone).attr('id', 'ac-techno-executive-'+value.le_id);
            $('.techno_executive_id', clone).addClass('group_le_'+value.ct_id);
            $('.old_executive_id', clone).attr('id', 'old_executive_id_'+value.le_id);
            $('.old_executive_id', clone).val(value.executive_id);

            

            $('.tm-techno-executive-name', clone).keyup(function(e){
                var condition_fields = ["country_domains"];
                var condition_values1 = [value.c_id];
                var condition_values2 = value.d_ids;

                var text_val = $(this).val();
                selected_textbox = $(this);
                selected_textid = $("#techno_executive_id_"+value.le_id);

                commonAutoComplete1(
                    e, $("#ac-techno-executive-"+value.le_id), $("#techno_executive_id_"+value.le_id), text_val,
                    TECHNO_USERS, "employee_name", "user_id", function (val) {
                        onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                    }, condition_fields, condition_values1, condition_values2);
            });
        
            $('.tbody-tm-view').append(clone);
        });

        console.log(group_countries)
        console.log(group_domains)
        $('.tm-group-checkbox').on('click', function(e) {
            var tm_view = '.tm-ac-' + $(this).val();
            var te_view = '.te-ac-' + $(this).val();
            if($(this).prop("checked")){
                $(tm_view).show();
                $(te_view).show();
            }else{
                $(tm_view).hide();
                $(te_view).hide();
            }
        });
}

function loadTEList(){
        $.each(TechnoDetailsList, function(key, value) {
            var letableRow = $('#templates .te-view-row .te-view-le-row');
            var clone = letableRow.clone();

            $('.te-group-checkbox', clone).val(value.ct_id + '-' + value.le_id);
            $('.te-group', clone).text(value.ct_name);
            var bg_name = '-';
            if(value.bg_name != null){
                bg_name = value.bg_name;
            }
            $('.te-businessgroup', clone).text(bg_name);
            $('.te-country', clone).text(value.c_name);
            $('.te-le', clone).text(value.le_name);

            /*$('.old_executive_id', clone).attr('id', 'old_executive_id_'+value.le_id);
            $('.old_executive_id', clone).val(value.executive_id);*/

        
            $('.tbody-te-view').append(clone);
        });

        /*$('.tm-group-checkbox').on('click', function(e) {
            var tm_view = '.tm-ac-' + $(this).val();
            var te_view = '.te-ac-' + $(this).val();
            if($(this).prop("checked")){
                $(tm_view).show();
                $(te_view).show();
            }else{
                $(tm_view).hide();
                $(te_view).hide();
            }
        });*/
}

function loadDMList(){
    alert('ent')
/*        var LastGroup = '';
        var group_countries = {};
        var group_domains = {};

        $.each(DomainDetailsList, function(key, value) {
            if(LastGroup != value.ct_name){
                var grouptableRow = $('#templates .tm-view-row .tm-view-group-row');
                var clone = grouptableRow.clone();

                $('.tm-group-checkbox', clone).val(value.ct_id);
                $('.tm-group', clone).text(value.ct_name);
                $('.tm-ac-view', clone).addClass('tm-ac-'+value.ct_id);

                $('.tm-techno-manager-name', clone).attr('id', 'techno_manager_name_'+value.ct_id);
                $('.techno_manager_id', clone).attr('id', 'techno_manager_id_'+value.ct_id);
                $('.ac-techno-manager', clone).attr('id', 'ac-techno-manager-'+value.ct_id);

                $('.tm-techno-manager-name', clone).keyup(function(e){
                    var condition_fields = ["country_domains"];
                    var condition_values1 = [group_countries[value.ct_id]];
                    var condition_values2 = group_domains[value.ct_id];

                    var text_val = $(this).val();
                    selected_textbox = $(this);
                    selected_textid = $("#techno_manager_id_"+value.ct_id);

                    commonAutoComplete1(
                        e, $("#ac-techno-manager-"+value.ct_id), $("#techno_manager_id_"+value.ct_id), text_val,
                        TECHNO_MANAGERS, "employee_name", "user_id",  function (val) {
                            onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                        }, condition_fields, condition_values1, condition_values2);
                });

                $('.tbody-tm-view').append(clone);
                LastGroup = value.ct_name;

                group_countries[value.ct_id] = [];
                group_domains[value.ct_id] = [];
            }

            group_countries[value.ct_id] = group_countries[value.ct_id].push(value.c_id);
            group_domains[value.ct_id] = $.merge(group_domains[value.ct_id], value.d_ids);

            var letableRow = $('#templates .tm-view-row .tm-view-le-row');
            var clone = letableRow.clone();
            $('.tm-country', clone).text(value.c_name);
            $('.tm-le', clone).text(value.le_name);
            $('.te-ac-view', clone).addClass('te-ac-'+value.ct_id);

            $('.tm-techno-executive-name', clone).attr('id', 'techno_executive_name_'+value.le_id);
            $('.techno_executive_id', clone).attr('id', 'techno_executive_id_'+value.le_id);
            $('.ac-techno-executive', clone).attr('id', 'ac-techno-executive-'+value.le_id);
            $('.techno_executive_id', clone).addClass('group_le_'+value.ct_id);
            $('.old_executive_id', clone).attr('id', 'old_executive_id_'+value.le_id);
            $('.old_executive_id', clone).val(value.executive_id);

            

            $('.tm-techno-executive-name', clone).keyup(function(e){
                var condition_fields = ["country_domains"];
                var condition_values1 = [value.c_id];
                var condition_values2 = value.d_ids;

                var text_val = $(this).val();
                selected_textbox = $(this);
                selected_textid = $("#techno_executive_id_"+value.le_id);

                commonAutoComplete1(
                    e, $("#ac-techno-executive-"+value.le_id), $("#techno_executive_id_"+value.le_id), text_val,
                    TECHNO_USERS, "employee_name", "user_id", function (val) {
                        onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                    }, condition_fields, condition_values1, condition_values2);
            });
        
            $('.tbody-tm-view').append(clone);
        });

        console.log(group_countries)
        console.log(group_domains)
        $('.tm-group-checkbox').on('click', function(e) {
            var tm_view = '.tm-ac-' + $(this).val();
            var te_view = '.te-ac-' + $(this).val();
            if($(this).prop("checked")){
                $(tm_view).show();
                $(te_view).show();
            }else{
                $(tm_view).hide();
                $(te_view).hide();
            }
        });*/
}
function callTechnoUserInfo(userId, type){
    mirror.getTechnoUSerInfo(userId, function(error, response) {
        if (error == null) {
            TechnoDetailsList = response.t_user_info;
            if(type == 'TM'){
                loadTMList();
            }else{
                loadTEList();
            }
        } else {
            displayMessage(error);
        }
    });

}

function callDomainUserInfo(userId, groupId, legalentityId, domainId, type){
    mirror.getDomainUserInfo(userId, groupId, legalentityId, domainId, function(error, response) {
        if (error == null) {
            DomainDetailsList = response.d_user_info;
            if(type == 'DM'){
                loadDMList();
            }else{
                loadDEList();
            }
        } else {
            displayMessage(error);
        }
    });

}

function pageControls(){
    TechnoManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACTechnoManager, TechnoManagerId, text_val,
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(TechnoManagerName, TechnoManagerId, val);
            });
    });

    TechnoExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACTechnoExecutive, TechnoExecutiveId, text_val,
            TECHNO_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(TechnoExecutiveName, TechnoExecutiveId, val);
            });
    });

    RTechnoExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, RACTechnoExecutive, RTechnoExecutiveId, text_val,
            TECHNO_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RTechnoExecutiveName, RTechnoExecutiveId, val);
            });
    });

    TMShow.click(function(){
        if(TechnoManagerId.val() == ''){
            displayMessage(message.reassign_from_required)
        }else{
            callTechnoUserInfo(parseInt(TechnoManagerId.val()), 'TM');
        }
    });

    TEShow.click(function(){
        if(TechnoExecutiveId.val() == ''){
            displayMessage(message.reassign_from_required)
        }else{
            callTechnoUserInfo(parseInt(TechnoExecutiveId.val()), 'TE');
        }
    });

    DMShow.click(function(){
        var dm_id = DomainManagerId.val();
        var group_id = DMGroupId.val();
        var le_id = DMLegalEntityId.val();
        var domain_id = DMDomainId.val();

        if(dm_id == ''){
            displayMessage(message.reassign_from_required);
        }else if(group_id == ''){
            displayMessage(message.group_required);
        }else if(le_id == ''){
            displayMessage(message.legalentity_required);
        }else if(domain_id == ''){
            displayMessage(message.domain_required);
        }else{
            callDomainUserInfo(parseInt(dm_id), parseInt(group_id), parseInt(le_id), parseInt(domain_id), 'DM');
        }
    });


    Submit.click(function(){
        var reassignDetails = [];
        var reassign_from = TechnoManagerId.val();
        var tm_remarks = TMRemarks.val();
        var isValidate = false;

        if(reassign_from == ''){
            displayMessage(message.reassign_from_required);
            return false;
        }else{
            if($('.tm-group-checkbox:checkbox:checked').length > 0){
                $('.tm-group-checkbox:checkbox:checked').each(function (index, el) {
                    var group_id = $(this).val();
                    var reassign_to = $("#techno_manager_id_"+group_id).val();
                    if(reassign_to == ''){
                        displayMessage(message.reassign_to_tm_required)
                        return false;
                    }else{
                        $('.group_le_'+group_id).each(function (i, element) {
                            var selected_id = $(element).attr('id');
                            var legal_entity_id = selected_id.substr(selected_id.lastIndexOf('_') + 1);
                            var te_id = $(element).val();
                            var old_executive_id = $('#old_executive_id_'+legal_entity_id).val();

                            if(te_id == ''){
                                displayMessage(message.reassign_to_te_required);
                                return false;
                            }else{
                                if(tm_remarks == ''){
                                    displayMessage(message.remarks_required);
                                    return false;
                                }else{
                                    reassignDetailsData = mirror.technoManagerInfo(parseInt(reassign_to), parseInt(group_id),
                                        parseInt(legal_entity_id), parseInt(te_id), parseInt(old_executive_id));
                                    reassignDetails.push(reassignDetailsData);
                                    isValidate = true;
                                    
                                }
                            }
                        });
                    }
                });
                if(isValidate){
                    mirror.ReassignTechnoManager(parseInt(reassign_from), reassignDetails, tm_remarks, 
                        function(error, response) {
                        if (error == null) {
                            displaySuccessMessage(message.reassign_users_account_success);
                        } else {
                            displayMessage(error);
                        }
                    });
                }
                
            }else{
                displayMessage(message.no_records_selected_for_reassign);
            }
            
        }
    });

    TESubmit.click(function(){
        var reassignDetails = [];
        var reassign_from = TechnoExecutiveId.val();
        var reassign_to = RTechnoExecutiveId.val();
        var te_remarks = TERemarks.val();
        var isValidate = false;

        if(reassign_from == ''){
            displayMessage(message.reassign_from_required);
            return false;
        }else{
            if($('.te-group-checkbox:checkbox:checked').length > 0){
                $('.te-group-checkbox:checkbox:checked').each(function (index, el) {
                    var combile_id = $(this).val().split('-');
                    var group_id = combile_id[0];
                    var le_id = combile_id[1];
                    
                    if(reassign_to == ''){
                        displayMessage(message.reassign_to_te_required)
                        return false;
                    }else{
                        if(te_remarks == ''){
                            displayMessage(message.remarks_required);
                            return false;
                        }else{
                            reassignDetailsData = mirror.technoExecutiveInfo(parseInt(group_id),
                                parseInt(le_id));
                            reassignDetails.push(reassignDetailsData);
                            isValidate = true;
                        }
                    }
                });
                if(isValidate){
                    mirror.ReassignTechnoExecutive(parseInt(reassign_from), parseInt(reassign_to), 
                        reassignDetails, te_remarks, 
                        function(error, response) {
                        if (error == null) {
                            displaySuccessMessage(message.reassign_users_account_success);
                        } else {
                            displayMessage(error);
                        }
                    });
                }
                
            }else{
                displayMessage(message.no_records_selected_for_reassign);
            }
            
        }
    });

    DMSubmit.click(function(){
        var reassignDetails = [];
        var reassign_from = TechnoExecutiveId.val();
        var reassign_to = RTechnoExecutiveId.val();
        var te_remarks = TERemarks.val();
        var isValidate = false;

        if(reassign_from == ''){
            displayMessage(message.reassign_from_required);
            return false;
        }else{
            if($('.te-group-checkbox:checkbox:checked').length > 0){
                $('.te-group-checkbox:checkbox:checked').each(function (index, el) {
                    var combile_id = $(this).val().split('-');
                    var group_id = combile_id[0];
                    var le_id = combile_id[1];
                    
                    if(reassign_to == ''){
                        displayMessage(message.reassign_to_te_required)
                        return false;
                    }else{
                        if(te_remarks == ''){
                            displayMessage(message.remarks_required);
                            return false;
                        }else{
                            reassignDetailsData = mirror.technoExecutiveInfo(parseInt(group_id),
                                parseInt(le_id));
                            reassignDetails.push(reassignDetailsData);
                            isValidate = true;
                        }
                    }
                });
                if(isValidate){
                    mirror.ReassignTechnoExecutive(parseInt(reassign_from), parseInt(reassign_to), 
                        reassignDetails, te_remarks, 
                        function(error, response) {
                        if (error == null) {
                            displaySuccessMessage(message.reassign_users_account_success);
                        } else {
                            displayMessage(error);
                        }
                    });
                }
                
            }else{
                displayMessage(message.no_records_selected_for_reassign);
            }
            
        }
    });


    DomainManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainManager, DomainManagerId, text_val,
            DOMAIN_MANAGERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(DomainManagerName, DomainManagerId, val);
            });
    });

    DMGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_closed"];
        var condition_values = [false];
        commonAutoComplete(
            e, DMACGroup, DMGroupId, text_val,
            GROUPS, "group_name", "group_id", function (val) {
                onAutoCompleteSuccess(DMGroupName, DMGroupId, val);
            }, condition_fields, condition_values);
    });

    DMBusinessGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if(DMGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DMGroupId.val());
        }
        commonAutoComplete(
            e, DMACBusinessGroup, DMBusinessGroupId, text_val,
            BUSINESS_GROUPS, "business_group_name", "business_group_id",
            function (val) {
                onAutoCompleteSuccess(DMBusinessGroupName, DMBusinessGroupId, val);
            }, condition_fields, condition_values);
    });

    DMLegalEntityName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if(DMGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DMGroupId.val());
        }
        if(DMBusinessGroupId.val() != ''){
            condition_fields.push("business_group_id");
            condition_values.push(DMBusinessGroupId.val());
        }
        commonAutoComplete(
            e, DMACLegalEntity, DMLegalEntityId, text_val,
            LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
            function (val) {
                onAutoCompleteSuccess(DMLegalEntityName, DMLegalEntityId, val)
            }, condition_fields, condition_values);
    })

    DMDomainName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, DMACDomain, DMDomainId, text_val,
            DOMAINS, "domain_name", "domain_id",
            function (val) {
                onAutoCompleteSuccess(DMDomainName, DMDomainId, val)
            }, condition_fields, condition_values);
    });

    /*RTTechnoManagerName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, ACRTTechnoManager, RTTechnoManagerId, text_val,
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RTTechnoManagerName, RTTechnoManagerId, val);
            }, condition_fields, condition_values);
    });
    TechnoUserName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, ACTechnoUser, TechnoUserId, text_val,
            TECHNO_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(TechnoUserName, TechnoUserId, val);
            }, condition_fields, condition_values);
    });
    RTTechnoUserName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, ACRTTechnoUser, RTTechnoUserId, text_val,
            TECHNO_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RTTechnoUserName, RTTechnoUserId, val);
            }, condition_fields, condition_values);
    });
    
    RTDomainManagerName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, ACRTDomainManager, RTDomainManagerId, text_val,
            DOMAIN_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(RTDomainManagerName, RTDomainManagerId, val);
        }, condition_fields, condition_values);
    });
    DomainExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, ACDomainExecutive, DomainExecutiveId, text_val,
            DOMAIN_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(DomainExecutiveName, DomainExecutiveId, val);
            }, condition_fields, condition_values);
    });
    RTDomainExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, ACRTDomainExecutive, RTDomainExecutiveId, text_val,
            DOMAIN_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RTDomainExecutiveName, RTDomainExecutiveId, val);
            }, condition_fields, condition_values);
    });
    GroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, ACGroup, GroupId, text_val,
            GROUPS, "group_name", "group_id", function (val) {
                onAutoCompleteSuccess(GroupName, GroupId, val);
            }, condition_fields, condition_values);
    });
    BusinessGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if(GroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(GroupId.val());
        }
        commonAutoComplete(
            e, ACBusinessGroup, BusinessGroupId, text_val,
            BUSINESS_GROUPS, "business_group_name", "business_group_id",
            function (val) {
                onAutoCompleteSuccess(BusinessGroupName, BusinessGroupId, val);
            }, condition_fields, condition_values);
    });
    
    Show.click(function(){
        validateAndShowList();
    });
    Submit.click(function(){
        validateAndSave();
    });
    UnitHeaderCheckBox.change(function(){
        activateOrDeactivateAllUnit();
    });
    EntityHeaderCheckBox.change(function(){
        activateOrDeactivateAllEntity();
    });
    GroupHeaderCheckBox.change(function(){
        activateOrDeactivateAllGroup();
    });*/
}

/*function validateAndShowList(){
    val_user_type = UserType.val();
    val_techno_manager_id = TechnoManagerId.val();
    val_techno_executive_id = TechnoUserId.val();
    val_domain_manager_id = DomainManagerId.val();
    val_domain_executive_id = DomainExecutiveId.val();
    val_group_id = GroupId.val();
    val_business_group_id = BusinessGroupId.val();
    val_legal_entity_id = EntityId.val();
    val_domain_id = DomainId.val();
    var validation_result = true;

    if(val_user_type == 5){
        if(val_techno_manager_id.trim().length == 0){
            displayMessage(message.techno_manager_required);
            validation_result = false;
        }
    }else if (val_user_type == 6){
        if(val_techno_executive_id.trim().length == 0){
            displayMessage(message.techno_executive_required);
            validation_result = false;
        }
    }else{
        if(val_user_type == 7){
            if(val_domain_manager_id.trim().length == 0){
                displayMessage(message.domain_manager_required);
                validation_result = false;
            }
        }else if(val_user_type == 8){
            if(val_domain_executive_id.trim().length == 0){
                displayMessage(message.domain_executive_required);
                validation_result = false;
            }
        }
        if(validation_result == true){
            if(val_group_id.trim().length == 0){
                displayMessage(message.group_required);
                validation_result = false;
            }else if(val_legal_entity_id.trim().length == 0){
                displayMessage(message.legalentity_required);
                validation_result = false;
            }else if(val_domain_id.trim().length == 0){
                displayMessage(message.domain_required);
                validation_result = false;
            }
        }
    }
    if(validation_result == true){
        loadAssignList();
    }
}

function clearGrids(){
    GroupView.hide();
    LegalEntityView.hide();
    UnitView.hide();
    ReassignToTechnoManager.hide();
    ReassignToTechnoUser.hide();
    ReassignToDomainManager.hide();
    ReassignToDomainUser.hide();
    RemarksDiv.hide();
    Submit.hide();
}

function loadAssignList(){
    ViewNote.show();
    RemarksDiv.show();
    Submit.show();
    if(val_user_type == 5){
        GroupView.show();
        LegalEntityView.hide();
        UnitView.hide();
        ReassignToTechnoManager.show();
        ReassignToTechnoUser.hide();
        ReassignToDomainManager.hide();
        ReassignToDomainUser.hide();
        loadGroupList();
    }else if(val_user_type == 6){
        GroupView.hide();
        LegalEntityView.show();
        UnitView.hide();
        ReassignToTechnoManager.hide();
        ReassignToTechnoUser.show();
        ReassignToDomainManager.hide();
        ReassignToDomainUser.hide();
        loadLegalEntity();
    }else{
        GroupView.hide();
        LegalEntityView.hide();
        UnitView.show();
        ReassignToTechnoManager.hide();
        ReassignToTechnoUser.hide();
        if(val_user_type == 3){
            ReassignToDomainManager.show();
            ReassignToDomainUser.hide();
        }else{
            ReassignToDomainManager.hide();
            ReassignToDomainUser.show();
        }
        loadUnits();
    }
}

function loadGroupList(){
    GroupCheckBoxes = {};
    TBodyReassignListGroupView.empty();
    var assigned_clients = user_wise_clients[val_techno_manager_id];
    $.each(GROUPS, function(key, value){
        if(assigned_clients.indexOf(value.group_id) > -1){
            var clone = GroupViewRow.clone();
            $(CountryNames, clone).text(value.country_names);
            $(Group_Name, clone).text(value.group_name);
            $(LECount, clone).text(value.no_of_legal_entities);
            GroupCheckBoxes[value.group_id] = false;
            $(GroupCheckBox, clone).addClass("group-"+value.group_id);
            TBodyReassignListGroupView.append(clone);
            $(GroupCheckBox, clone).change(function(){
                activateOrDeactivateGroup(value.group_id);
            });
        }
    });
}

function activateOrDeactivateGroup(group_id){
    group_status = $(".group-"+group_id).prop("checked");
    GroupCheckBoxes[group_id] = group_status;
}

function loadLegalEntity(){
    EntityCheckBoxes = {};
    TBodyReassignListLegalEntityView.empty();
    var entities_assigned_to_selected_user = user_wise_entities[val_techno_executive_id];
    $.each(LEGAL_ENTITIES, function(key, value){
        if(entities_assigned_to_selected_user != undefined && entities_assigned_to_selected_user.indexOf(value.legal_entity_id) > -1 ){
            var clone = LegalEntityViewRow.clone();
            $(Group_Name, clone).text(client_id_name_map[value.group_id]);
            $(BG_Name, clone).text(business_group_id_name_map[value.business_group_id]);
            $(Country, clone).text(country_id_name_map[value.country_id]);
            $(Entity, clone).text(value.legal_entity_name);
            $(EntityCheckBox, clone).addClass("entity-"+value.legal_entity_id);
            EntityCheckBoxes[value.legal_entity_id] = false;
            TBodyReassignListLegalEntityView.append(clone);
            $(EntityCheckBox, clone).change(function(){
                activateOrDeactivateEntity(value.legal_entity_id);
            });
        }
    });
}

function loadUserCategory(){
    $.each(USER_CATEGORIES, function(k, val){
        var obj = $(".usertype-drop-down option");
        var clone = obj.clone();
        clone.attr("value", val["user_category_id"]);
        clone.text(val["user_category_name"]);
        UserType.append(clone);
    });
}

function activateOrDeactivateEntity(legal_entity_id){
    entity_status = $(".entity-"+legal_entity_id).prop("checked");
    EntityCheckBoxes[legal_entity_id] = entity_status;
}

function loadUnits(){
    UnitCheckBoxes = {};
    TBodyReassignListUnitView.empty();
    var assigned_units_of_selected_user = [];
    if(val_domain_executive_id in user_wise_units){
        assigned_units_of_selected_user = user_wise_units[val_domain_executive_id][val_domain_id]
        if(val_user_type == 7)
            assigned_units_of_selected_user = user_wise_units[val_domain_manager_id][val_domain_id]
    }

    if(val_user_type == 7 && val_domain_manager_id in user_wise_units && user_wise_units[val_domain_manager_id][val_domain_id] != undefined){
        assigned_units_of_selected_user = user_wise_units[val_domain_manager_id][val_domain_id]
    }

    if(val_user_type == 8 && val_domain_executive_id in user_wise_units && user_wise_units[val_domain_executive_id][val_domain_id] != undefined){
        assigned_units_of_selected_user = user_wise_units[val_domain_executive_id][val_domain_id]
    }

    console.log(user_wise_units);
    console.log(assigned_units_of_selected_user);
    $.each(UNITS, function(key, value){
        if(
            assigned_units_of_selected_user.indexOf(value.unit_id) > -1 &&
            value.legal_entity_id == val_legal_entity_id &&
            value.client_id == val_group_id
        ){
            var clone = UnitViewRow.clone();
            $(UnitCode, clone).text(value.unit_code);
            $(UnitName, clone).text(value.unit_name);
            $(UnitLocation, clone).text(value.address);
            UnitCheckBoxes[value.unit_id] = false;
            $(UnitCheckBox, clone).addClass("unit-"+value.unit_id);
            TBodyReassignListUnitView.append(clone);
            $(UnitCheckBox, clone).change(function(){
                activateOrDeactivateUnit(value.unit_id);
            });
        }
    });
}

function activateOrDeactivateUnit(unit_id){
    unit_status = $(".unit-"+unit_id).prop("checked");
    UnitCheckBoxes[unit_id] = unit_status;
}

function activateOrDeactivateAllUnit(){
    unit_header_checkbox_stauts = UnitHeaderCheckBox.prop("checked");
    $.each(UnitCheckBoxes, function(key, value){
        $(".unit-"+key).prop("checked", unit_header_checkbox_stauts);
        UnitCheckBoxes[key] = unit_header_checkbox_stauts;
    });
}

function activateOrDeactivateAllEntity(){
    entity_header_checkbox_stauts = EntityHeaderCheckBox.prop("checked");
    $.each(EntityCheckBoxes, function(key, value){
        $(".entity-"+key).prop("checked", entity_header_checkbox_stauts);
        EntityCheckBoxes[key] = entity_header_checkbox_stauts;
    });
}

function activateOrDeactivateAllGroup(){
    group_header_checkbox_status = GroupHeaderCheckBox.prop("checked");
    $.each(GroupCheckBoxes, function(key, value){
        $(".group-"+key).prop("checked", group_header_checkbox_status);
        GroupCheckBoxes[key] = group_header_checkbox_status;
    });
}

function validateAndSave(){
    var check_box_list = [];
    var true_count = 0;
    var display_text = "";
    var ids = [];
    var reassign_to_user = '';
    var old_user = '';
    var user_validation_msg = '';
    var val_remarks = Remarks.val();
    if(val_user_type == 5){
        check_box_list = GroupCheckBoxes;
        display_text = "Group";
        reassign_to_user = RTTechnoManagerId.val();
        user_validation_msg = message.techno_manager_required;
        old_user = TechnoManagerId.val();
    }else if (val_user_type == 6){
        check_box_list = EntityCheckBoxes;
        display_text = "Legal Entity";
        reassign_to_user = RTTechnoUserId.val();
        user_validation_msg = message.techno_executive_required;
        old_user = TechnoUserId.val();
    }else if (val_user_type == 7 || val_user_type == 8){
        check_box_list = UnitCheckBoxes;
        display_text = "Unit";
        if(val_user_type == 7){
            reassign_to_user = RTDomainManagerId.val();
            user_validation_msg = message.domain_manager_required;
            old_user = DomainManagerId.val();
        }else{
            reassign_to_user = RTDomainExecutiveId.val();
            user_validation_msg = message.domain_executive_required;
            old_user = DomainExecutiveId.val();
        }
    }
    $.each(check_box_list, function(key, value){
        if(value == true){
            ++true_count;
            ids.push(parseInt(key));
        }

    });

    if(true_count <= 0){
        displayMessage("Select atleast one "+display_text);
    }else if(!reassign_to_user){
        displayMessage(user_validation_msg);
    }else if(val_remarks.trim() == 0){
        displayMessage(message.remarks_required);
    }else{
        function onSuccess(data) {
            displaySuccessMessage(message.reassign_users_account_success);
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveReassignUserAccount(
            parseInt(val_user_type), parseInt(old_user), parseInt(reassign_to_user), ids,
            val_remarks, function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }

}

function generateIdNameMaps(){
    $.each(GROUPS, function(key, value){
        client_id_name_map[value.client_id] = value.group_name;
    });
    $.each(COUNTRIES, function(key, value){
        country_id_name_map[value.country_id] = value.country_name;
    });
    $.each(BUSINESS_GROUPS, function(key, value){
        business_group_id_name_map[value.business_group_id] = value.business_group_name;
    });
    $.each(ASSIGNED_ENTITIES, function(key, value){
        if(!(value.user_id in user_wise_entities))
            user_wise_entities[value.user_id] = [];
        user_wise_entities[value.user_id].push(value.legal_entity_id);
    });
    $.each(ASSIGNED_UNITS, function(key, value){
        if(!(value.user_id in user_wise_units))
            user_wise_units[value.user_id] = {};
        if(!(value.domain_id in user_wise_units[value.user_id]))
            user_wise_units[value.user_id][value.domain_id] = [];

        user_wise_units[value.user_id][value.domain_id].push(value.unit_id);
    });
    $.each(ASSIGNED_CLIENTS, function(key, value){
        if(!(value.user_id in user_wise_clients))
            user_wise_clients[value.user_id] = [];
        user_wise_clients[value.user_id].push(value.client_id);
    });
}*/

function getFormData(){
    function onSuccess(data) {
        TECHNO_MANAGERS = data.t_m_reassign;
        TECHNO_USERS = data.t_e_reassign;
        DOMAIN_MANAGERS = data.d_m_reassign;
        DOMAIN_USERS = data.d_e_reassign;
        GROUPS = data.groups;
        BUSINESS_GROUPS = data.business_groups;
        LEGAL_ENTITIES = data.admin_legal_entity;
        DOMAINS = data.domains;
        USER_CATEGORIES = data.user_categories;
    }
    function onFailure(error) {
        custom_alert(error);
    }
    mirror.getReassignUserAccountFormdata(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

$(function(){
    initialize();
});

function initialize(){
    $(document).ready(function () {
        pageControls();
        getFormData();
        /*mirror.getTechnoUSerInfo(7, function(error, response) {

        });
        mirror.getDomainUserInfo(9, 1, 1, 1, function(error, response) {

        });*/
    });
}




