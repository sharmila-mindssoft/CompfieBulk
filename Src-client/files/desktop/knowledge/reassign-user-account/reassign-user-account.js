/* Elements */
var UserType = $("#usertype");
var Show = $(".btn-show");

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

// Techno User autocomplete
var TechnoUserDiv = $(".techno-user-div");
var TechnoUserName = $("#techno_user_name");
var TechnoUserId = $("#techno_user_id");
var ACTechnoUser = $("#ac-techno-user");

// Domain manager autocomplete
var DomainManagerDiv = $(".domain-mgr-div");
var DomainManagerName = $("#domain_manager_name");
var DomainManagerId = $("#domain_manager_id");
var ACDomainManager = $("#ac-domain-manager");

// Domain Executive autocomplete
var DomainUserDiv = $(".domain-user-div"); 
var DomainExecutiveName = $("#domain_executive_name");
var DomainExecutiveId = $("#domain_executive_id");
var ACDomainExecutive = $("#ac-domain-executive");

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

// Legal Entity View List
var LegalEntityView = $(".legalentity-view");
var TBodyReassignListLegalEntityView = $(".tbody-reassign-list-legalentity-view");

// Unit view List
var UnitView = $(".unit-view");
var TBodyReassignListUnitView = $(".tbody-reassign-list-unit-view");

var ReassignToTechnoManager = $(".reassign-tm");
var ReassignToTechnoUser = $(".reassign-tu");
var ReassignToDomainManager = $(".reassign-dm");
var ReassignToDomainUser = $(".reassign-du");

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


var TECHNO_MANAGERS = [
    {
        "user_id": 1,
        "employee_name": "Test 1"
    },
    {
        "user_id": 2,
        "employee_name": "Test 2"
    }
]

//retrive businessgroup form autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
}

function pageControls(){
    UserType.change(function(){
        user_type = UserType.val();
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
    TechnoUserName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACTechnoUser, TechnoUserId, text_val, 
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(TechnoUserName, TechnoUserId, val);
        });
    }); 
    DomainManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainManager, DomainManagerId, text_val, 
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(DomainManagerName, DomainManagerId, val);
        });
    });
    DomainExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainExecutive, DomainExecutiveId, text_val, 
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(DomainExecutiveName, DomainExecutiveId, val);
        });
    });
    GroupName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, GroupId, text_val, 
            TECHNO_MANAGERS, "group_name", "client_id", function (val) {
            onAutoCompleteSuccess(GroupName, GroupId, val);
        });
    });
    BusinessGroupName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACBusinessGroup, BusinessGroupId, text_val, 
            TECHNO_MANAGERS, "business_group_name", "business_group_id", 
            function (val) {
                onAutoCompleteSuccess(BusinessGroupName, BusinessGroupId, val);
        });
    });
    EntityName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACEntity, EntityId, text_val, 
            TECHNO_MANAGERS, "legal_entity_name", "legal_entity_id", 
            function (val) {
                onAutoCompleteSuccess(EntityName, EntityId, val);
        });
    })
    DomainName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomain, DomainId, text_val, 
            TECHNO_MANAGERS, "domain_name", "domain_id", 
            function (val) {
                onAutoCompleteSuccess(DomainName, DomainId, val);
        });
    });
    Show.click(function(){
        validateAndShowList();
    });
}

function validateAndShowList(){
    val_user_type = UserType.val();
    val_techno_manager_id = TechnoManagerId.val();
    val_techno_executive_id = TechnoUserId.val();
    val_domain_manager_id = DomainManagerId.val();
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
                displayMessage(message.domain_amnager_required);
                validation_result = false;
            }
        }else if(val_user_type == 4){
            if(val_domain_executive_id.trim().length == 0){
                displayMessage(message.domain_amnager_required);
                validation_result = false;
            }
        }
        if(val_group_id.trim().length == 0){
            displayMessage(message.group_required);
            validation_result = false;
        }else if(val_business_group_id.trim().length == 0){
            displayMessage(message.businessgroup_required);
            validation_result = false;
        }else if(val_legal_entity_id.trim().length == 0){
            displayMessage(message.legalentity_required);
            validation_result = false;
        }else if(val_domain_id.trim().length == 0){
            displayMessage(message.domain_required);
            validation_result = false;
        }
    }
    if(validation_result == true){
        loadAssignList();
    }
}

function loadAssignList(){
    $(".view-note").show();
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

}

function loadLegalEntity(){

}

function loadUnits(){

}

$(function(){
    initialize();
});

function initialize(){
    console.log("inside initialize")
    $(document).ready(function () {
        pageControls();
    });
}




