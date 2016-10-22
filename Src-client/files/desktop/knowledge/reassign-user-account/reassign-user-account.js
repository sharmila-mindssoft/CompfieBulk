/* Elements */
var UserType = $("#usertype");
var Show = $(".btn-show");
var Submit = $(".save");

// Group auto complete
var GroupDiv = $(".filter-group-div");
var GroupName = $("#group_name");
var GroupId = $("#group_id");
var ACGroup = $("#ac-group");

// Entity auto complete
var EntityDiv = $(".filter-legal-div");
var EntityName = $("#legal_entity_name");
var EntityId = $("#legal_entity_id");
var ACEntity = $("#ac-entity")

// Techno manager autocomplete
var TechnoManagerDiv = $(".techno-mgr-div");
var TechnoManagerName = $("#techno_manager_name");
var TechnoManagerId = $("#techno_manager_id");
var ACTechnoManager = $("#ac-techno-manager");
var RTTechnoManagerName = $("#rt_techno_manager_name");
var RTTechnoManagerId = $("#rt_techno_manager_id");
var ACRTTechnoManager = $("#ac-rt-techno-manager");

// Techno User autocomplete
var TechnoUserDiv = $(".techno-user-div");
var TechnoUserName = $("#techno_user_name");
var TechnoUserId = $("#techno_user_id");
var ACTechnoUser = $("#ac-techno-user");
var RTTechnoUserName = $("#rt_techno_user_name");
var RTTechnoUserId = $("#rt_techno_user_id");
var ACRTTechnoUser = $("#ac-rt-techno-user");

// Domain manager autocomplete
var DomainManagerDiv = $(".domain-mgr-div");
var DomainManagerName = $("#domain_manager_name");
var DomainManagerId = $("#domain_manager_id");
var ACDomainManager = $("#ac-domain-manager");
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
var BusinessGroupName = $("#business_group_name");
var BusinessGroupId = $("#business_group_id");
var ACBusinessGroup = $("#ac-business-group");

// Domain auto complete
var DomainDiv = $(".filter-domain-div");
var DomainName = $("#domain_name");
var DomainId = $("#domain_id");
var ACDomain = $("#ac-domain");

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
var client_id_name_map = {};
var country_id_name_map = {};
var business_group_id_name_map = {};
var user_wise_entities = {};
var user_wise_units = {};
var user_wise_clients = {};

var GroupCheckBoxes = {};
var EntityCheckBoxes = {};
var UnitCheckBoxes = {};

//retrive businessgroup form autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
}

function pageControls(){
    UserType.change(function(){
        user_type = UserType.val();
        clearGrids();
        if(user_type == 1){ // Techno Manager
            TechnoManagerDiv.show();
            TechnoUserDiv.hide();
            DomainManagerDiv.hide();
            GroupDiv.hide();
            BusinessGroupDiv.hide();
            EntityDiv.hide();
            DomainDiv.hide();
            DomainUserDiv.hide();
        }else if(user_type == 2){ // Techno User
            TechnoManagerDiv.hide();
            TechnoUserDiv.show();
            DomainManagerDiv.hide();
            GroupDiv.hide();
            BusinessGroupDiv.hide();
            EntityDiv.hide();
            DomainDiv.hide();
            DomainUserDiv.hide();
        }else if(user_type == 3){ // Domain Manager
            TechnoManagerDiv.hide();
            TechnoUserDiv.hide();
            DomainManagerDiv.show();
            GroupDiv.show();
            BusinessGroupDiv.show();
            EntityDiv.show();
            DomainDiv.show();
            DomainUserDiv.hide();
        }else if(user_type == 4){ // Domain User
            TechnoManagerDiv.hide();
            TechnoUserDiv.hide();
            DomainManagerDiv.hide();
            GroupDiv.show();
            BusinessGroupDiv.show();
            EntityDiv.show();
            DomainDiv.show();
            DomainUserDiv.show();
        }
    });

    TechnoManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACTechnoManager, TechnoManagerId, text_val, 
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(TechnoManagerName, TechnoManagerId, val);
        });
    });
    RTTechnoManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACRTTechnoManager, RTTechnoManagerId, text_val, 
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(RTTechnoManagerName, RTTechnoManagerId, val);
        });
    });
    TechnoUserName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACTechnoUser, TechnoUserId, text_val, 
            TECHNO_USERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(TechnoUserName, TechnoUserId, val);
        });
    }); 
    RTTechnoUserName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACRTTechnoUser, RTTechnoUserId, text_val, 
            TECHNO_USERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(RTTechnoUserName, RTTechnoUserId, val);
        });
    }); 
    DomainManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainManager, DomainManagerId, text_val, 
            DOMAIN_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(DomainManagerName, DomainManagerId, val);
        });
    });
    RTDomainManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACRTDomainManager, RTDomainManagerId, text_val, 
            DOMAIN_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(RTDomainManagerName, RTDomainManagerId, val);
        });
    });
    DomainExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainExecutive, DomainExecutiveId, text_val, 
            DOMAIN_USERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(DomainExecutiveName, DomainExecutiveId, val);
        });
    });
    RTDomainExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACRTDomainExecutive, RTDomainExecutiveId, text_val, 
            DOMAIN_USERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(RTDomainExecutiveName, RTDomainExecutiveId, val);
        });
    });
    GroupName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, GroupId, text_val, 
            GROUPS, "group_name", "client_id", function (val) {
            onAutoCompleteSuccess(GroupName, GroupId, val);
        });
    });
    BusinessGroupName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACBusinessGroup, BusinessGroupId, text_val, 
            BUSINESS_GROUPS, "business_group_name", "business_group_id", 
            function (val) {
                onAutoCompleteSuccess(BusinessGroupName, BusinessGroupId, val);
        });
    });
    EntityName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACEntity, EntityId, text_val, 
            LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id", 
            function (val) {
                onAutoCompleteSuccess(EntityName, EntityId, val);
        });
    })
    DomainName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomain, DomainId, text_val, 
            DOMAINS, "domain_name", "domain_id", 
            function (val) {
                onAutoCompleteSuccess(DomainName, DomainId, val);
        });
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
    });
}

function validateAndShowList(){
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
    if(val_user_type == 1){
        if(val_techno_manager_id.trim().length == 0){
            displayMessage(message.techno_manager_required);
            validation_result = false;
        }
    }else if (val_user_type == 2){
        if(val_techno_executive_id.trim().length == 0){
            displayMessage(message.techno_executive_required);
            validation_result = false;
        }
    }else{
        if(val_user_type == 3){
            if(val_domain_manager_id.trim().length == 0){
                displayMessage(message.domain_manager_required);
                validation_result = false;
            }
        }else if(val_user_type == 4){
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
    if(val_user_type == 1){
        GroupView.show();
        LegalEntityView.hide();
        UnitView.hide();
        ReassignToTechnoManager.show();
        ReassignToTechnoUser.hide();
        ReassignToDomainManager.hide();
        ReassignToDomainUser.hide();
        loadGroupList();
    }else if(val_user_type == 2){
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
        if(entities_assigned_to_selected_user.indexOf(value.legal_entity_id) > -1){
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
        if(val_user_type == 3)
            assigned_units_of_selected_user = user_wise_units[val_domain_manager_id][val_domain_id]
    }
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
    if(val_user_type == 1){
        check_box_list = GroupCheckBoxes;
        display_text = "Group";
        reassign_to_user = RTTechnoManagerId.val();
        user_validation_msg = message.techno_manager_required;
        old_user = TechnoManagerId.val();
    }else if (val_user_type == 2){
        check_box_list = EntityCheckBoxes;
        display_text = "Legal Entity";
        reassign_to_user = RTTechnoUserId.val();
        user_validation_msg = message.techno_executive_required;
        old_user = TechnoUserId.val();
    }else if (val_user_type == 3 || val_user_type == 4){
        check_box_list = UnitCheckBoxes;
        display_text = "Unit";
        if(val_user_type == 3){
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
        }
        ids.push(parseInt(key));
    });

    if(true_count <= 0){
        displayMessage("Select atleast one "+display_text);
    }else if(!reassign_to_user){
        displayMessage(user_validation_msg);
    }else if(val_remarks.trim() == 0){
        displayMessage(message.remarks_required);
    }else{
        function onSuccess(data) {
            displayMessage(message.reassign_users_account_success);
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
            user_wise_units[value.user_id][domain_id] = [];
        user_wise_units[value.user_id][domain_id].push(value.unit_id);
    });
    $.each(ASSIGNED_CLIENTS, function(key, value){
        if(!(value.user_id in user_wise_clients))
            user_wise_clients[value.user_id] = [];
        user_wise_clients[value.user_id].push(value.client_id);
    });
}

function getFormData(){
    function onSuccess(data) {
        TECHNO_MANAGERS = data.techno_managers;
        TECHNO_USERS = data.techno_users;
        DOMAIN_MANAGERS = data.domain_managers;
        DOMAIN_USERS = data.domain_users;
        GROUPS = data.groups;
        BUSINESS_GROUPS = data.business_groups;
        LEGAL_ENTITIES = data.admin_legal_entity;
        UNITS = data.unit_id_name;
        COUNTRIES = data.countries;
        DOMAINS = data.domains;
        ASSIGNED_ENTITIES = data.assigned_legal_entities;
        ASSIGNED_UNITS = data.assigned_units;
        ASSIGNED_CLIENTS = data.assigned_clients;
        generateIdNameMaps();
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
    });
}




