var DOMAIN_ID = '';
var CLIENT_ID = '';
var DOMAIN_NAME = '';
var GROUP_NAME = '';
var UNASSIGNED_UNITS ='';
var LEGAL_ENTITY_ID = '';
var LEGAL_ENTITY_NAME = '';
var BUSINESS_GROUP_NAME = '';
var BUSINESS_GROUP_ID = '';
var ASSIGNED_UNIT_DETAILS_LIST = '';
var ORGANIZED_DETAILS_LIST = '';
var BUSINESS_GROUPS = '';
var DOMAIN_MANAGER_USERS = '';
var LEGAL_ENTITIES = '';
var ASSIGN_UNIT_SAVE_DETAILS = {};
var LEGAL_ENTITY_UNIT_MAP = {};

function clearForm(){
    DOMAIN_ID = '';
    CLIENT_ID = '';
    DOMAIN_NAME = '';
    GROUP_NAME = '';
    UNASSIGNED_UNITS ='';
    LEGAL_ENTITY_ID = '';
    LEGAL_ENTITY_NAME = '';
    BUSINESS_GROUP_NAME = '';
    BUSINESS_GROUP_ID = '';
    ASSIGNED_UNIT_DETAILS_LIST = '';
    ORGANIZED_DETAILS_LIST = '';
    BUSINESS_GROUPS = '';
    DOMAIN_MANAGER_USERS = '';
    LEGAL_ENTITIES = '';
    ASSIGN_UNIT_SAVE_DETAILS = {};
    LEGAL_ENTITY_UNIT_MAP = {};
    $("#businessgroupsval").val("");
    $("#businessgroupid").val("");
    $("#legalentityval").val("");
    $("#legalentityid").val("");
    $("#assinee").val("");
    $("#userid").val("");
    $(".unassign-list").empty();
    $(".assigned-list").empty();
    $(".assigned-unit-view-list").empty();
    $(".assigned-unit-edit-list").empty();
    $("#edit-legal-entity").hide();
}

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        clearForm();
        function onSuccess(data) {
            UNASSIGNED_UNITS = data["unassigned_units_list"];
            loadUnAssignedUnitsList();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getUnassignedUnitsList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else if(type_of_form == "assign"){
        function onSuccess(data) {
            BUSINESS_GROUPS = data.business_groups;
            ASSIGNED_UNIT_DETAILS_LIST = data.assigned_unit_details_list;
            DOMAIN_MANAGER_USERS = data.domain_manager_users;
            LEGAL_ENTITIES = data.unit_legal_entity;
            loadAssignUnitForm();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getAssignUnitFormData(
            DOMAIN_ID, CLIENT_ID,function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else if(type_of_form == "view"){
        function onSuccess(data) {
            ASSIGNED_UNITS = data["assigned_units_list"];
            loadAssignedUnitsList();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getAssignedUnitsList(
            DOMAIN_ID, CLIENT_ID,function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else if(type_of_form == "view-details"){
        function onSuccess(data) {
            ASSIGNED_UNIT_DETAILS_LIST = data.assigned_unit_details_list
            loadAssignedUnitsDetailsList();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getAssignedUnitDetails(
            LEGAL_ENTITY_ID, DOMAIN_MANAGER_ID, function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }
}

function showPage(type_of_form){
    if(type_of_form == "list"){
        $("#unassigned_units").show();
        $("#assigned_units").hide();
        $("#assign").hide();
        $("#view-details").hide();
    }else if(type_of_form == "assign"){
        $("#unassigned_units").hide();
        $("#assigned_units").hide();
        $("#assign").show();
        $("#view-details").hide();
    }else if(type_of_form == "view"){
        $("#unassigned_units").hide();
        $("#assigned_units").show();
        $("#assign").hide();
        $("#view-details").hide();
    }else if(type_of_form == "view-details"){
        $("#unassigned_units").hide();
        $("#assigned_units").hide();
        $("#assign").hide();
        $("#view-details").show();
    }
}

$(".cancel-view-details").click(function(){
    initialize("view");
});

$(".btn-back").click(function(){
    initialize("list");
});

$(".cancel-assign-unit").click(function(){
    initialize("list");
});

function loadUnAssignedUnitsList(){
    $(".unassign-list").empty();
    var row = $("#templates .unassign-row tr");
    var sno = 0;
    $.each(UNASSIGNED_UNITS, function(key, value){
        ++sno;
        var clone = row.clone();
        $(".sno", clone).text(sno);
        $(".domain-name", clone).text(value.domain_name);
        $(".group-name", clone).text(value.group_name);
        $(".unassigned-units", clone).text(value.unassigned_units);
        $(".assign", clone).click(function(){
            viewAssignUnitsForm(
                value.domain_id, value.client_id,
                value.domain_name, value.group_name
            );
        });
        $(".view", clone).click(function(){
            viewDomainManagers(
                value.domain_id, value.client_id,
                value.domain_name, value.group_name
            );
        });
        $(".unassign-list").append(clone);
    });
}

function viewAssignUnitsForm(domain_id, client_id, domain_name, group_name){
    DOMAIN_ID = domain_id;
    CLIENT_ID = client_id;
    DOMAIN_NAME = domain_name;
    GROUP_NAME = group_name;
    initialize("assign");
}

function viewDomainManagers(domain_id, client_id, domain_name, group_name){
    DOMAIN_ID = domain_id;
    CLIENT_ID = client_id;
    DOMAIN_NAME = domain_name;
    GROUP_NAME = group_name;
    initialize("view");
}

function loadAssignedUnitsList(){
    $(".assigned-list").empty();
    var row = $("#templates .assigned-row tr");
    var sno = 0;
    $.each(ASSIGNED_UNITS, function(key, value){
        ++sno;
        var clone = row.clone();
        $(".sno", clone).text(sno);
        $(".domain-manager", clone).text(value.employee_name);
        $(".domain-name", clone).text(DOMAIN_NAME);
        $(".group-name", clone).text(GROUP_NAME);
        $(".business-group-name", clone).text(value.business_group_name);
        $(".legal-entity-name", clone).text(value.legal_entity_name);
        $(".no-of-units", clone).text(value.unit_count);
        $(".view", clone).click(function(){
            viewAssignedUnitDetails(
                value.business_group_name, value.legal_entity_name,
                value.legal_entity_id, value.user_id
            );
        });
        $(".assigned-list").append(clone);
    });
}

function viewAssignedUnitDetails(
    business_group_name, legal_entity_name,
    legal_entity_id, user_id
){
    BUSINESS_GROUP_NAME = business_group_name;
    LEGAL_ENTITY_NAME = legal_entity_name;
    LEGAL_ENTITY_ID = legal_entity_id;
    DOMAIN_MANAGER_ID = user_id
    initialize("view-details")
}

function loadAssignedUnitsDetailsList(){
    $(".view-grop-name").text(GROUP_NAME);
    $(".view-bg-name").text(BUSINESS_GROUP_NAME);
    $(".view-domain-name").text(DOMAIN_NAME);
    $(".le-name").text(LEGAL_ENTITY_NAME);
    ORGANIZED_DETAILS_LIST = {}
    $.each(ASSIGNED_UNIT_DETAILS_LIST, function(key, value){
        var legal_entity_name = value["legal_entity_name"];
        var division_name = value["division_name"];
        var category_name = value["category_name"]
        if(! (legal_entity_name in ORGANIZED_DETAILS_LIST)){
            ORGANIZED_DETAILS_LIST[legal_entity_name] = {}
        }
        if(! (division_name in ORGANIZED_DETAILS_LIST[legal_entity_name])){
            ORGANIZED_DETAILS_LIST[legal_entity_name][division_name] = {}
        }
        if(! (category_name in ORGANIZED_DETAILS_LIST[legal_entity_name][division_name])){
            ORGANIZED_DETAILS_LIST[legal_entity_name][division_name][category_name] = []
        }
        ORGANIZED_DETAILS_LIST[legal_entity_name][division_name][category_name].push(
            value
        )
    });
    var header_row = $("#templates .assigned-unit-view-row-header tr");
    var content_row = $("#templates .assigned-unit-view-row tr");
    var bold_text = $("#templates .bold-text");
    var normal_text = $("#templates .normal-text");
    $(".assigned-unit-view-list").empty();
    $.each(ORGANIZED_DETAILS_LIST, function(legal_entity_name, entity_value){
        $.each(entity_value, function(division_name, div_value){
            $.each(div_value, function(category_name, cat_value){
                var header_clone = header_row.clone();
                $(".view-le-name", header_clone).text("Legal Entity :- "+legal_entity_name);
                $(".view-div-name", header_clone).text("Division :- "+returnHyphenIfNull(division_name));
                $(".view-category-name", header_clone).text("Category :- "+returnHyphenIfNull(category_name));
                $(".assigned-unit-view-list").append(header_clone);
                $.each(cat_value, function(key, value){
                    var row_clone = content_row.clone();
                    $(".unit-code", row_clone).text(value.unit_code);
                    $(".unit-name .address", row_clone).text(value.unit_name);
                    $(".unit-name .address-title", row_clone).attr("title", value.address);
                    $(".unit-name .address-title", row_clone).attr("title", value.address);
                    $(".organization-type", row_clone).empty();
                    $.each(value.domain_names, function(key, d_value){
                        var clone = bold_text.clone();
                        clone.text(d_value);

                        $(".organization-type", row_clone).append(clone);
                        $.each(value.org_names_list[key], function(key, org_value){
                            var clone1 = bold_text.clone();
                            clone1.text(org_value);
                            $(".organization-type", row_clone).append(clone1);
                        });
                    });
                    $(".location", row_clone).text(value.geography_name);
                    $(".assigned-unit-view-list").append(row_clone);
                });
            });
        });
    });
}

function returnHyphenIfNull(value){
    if(value == null){
        return " - "
    }else{
        return value
    }
}

//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val) {
  $('#businessgroupsval').val(val[1]);
  $('#businessgroupid').val(val[0]);
}
//load businessgroup form list in autocomplete text box  
$('#businessgroupsval').keyup(function (e) {
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(e, textval, BUSINESS_GROUPS, function (val) {
    onBusinessGroupSuccess(val);
  });
});

//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val) {
  $('#legalentityval').val(val[1]);
  $('#legalentityid').val(val[0]);
}
//load legalentity form list in autocomplete text box  
$('#legalentityval').keyup(function (e) {
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(e, textval, LEGAL_ENTITIES, function (val) {
    onLegalEntitySuccess(val);
  });
});

//retrive user form autocomplete value
function onUserSuccess(val) {
    $('#assinee').val(val[1]);
    $('#userid').val(val[0]);
}
//load legalentity form list in autocomplete text box  
$('#assinee').keyup(function (e) {
  var textval = $(this).val();
  getUserAutocomplete(e, textval, DOMAIN_MANAGER_USERS, function (val) {
    onUserSuccess(val);
  });
});

function loadAssignUnitForm(){
    $(".edit-group-name").text(GROUP_NAME);
    $(".edit-domain-name").text(DOMAIN_NAME);
}

$(".show-units").click(function(){
    LEGAL_ENTITY_NAME = $("#legalentityval").val();
    BUSINESS_GROUP_NAME = $("#businessgroupsval").val();
    BUSINESS_GROUP_ID = $("#businessgroupid").val();
    loadEditAssignedUnitsDetailsList();
});

function loadEditAssignedUnitsDetailsList(){
    ORGANIZED_DETAILS_LIST = {}
    $.each(ASSIGNED_UNIT_DETAILS_LIST, function(key, value){
        var legal_entity_name = value["legal_entity_name"];
        var division_name = value["division_name"];
        var category_name = value["category_name"]
        var validation_status = false;
        if (LEGAL_ENTITY_NAME != '' || LEGAL_ENTITY_NAME == legal_entity_name){
            validation_status = true;
        }
        if (value["business_group_id"]  == BUSINESS_GROUP_ID){
            validation_status = true;
        }
        if(validation_status){
            if(! (legal_entity_name in ORGANIZED_DETAILS_LIST)){
                ORGANIZED_DETAILS_LIST[legal_entity_name] = {}
            }
            if(! (division_name in ORGANIZED_DETAILS_LIST[legal_entity_name])){
                ORGANIZED_DETAILS_LIST[legal_entity_name][division_name] = {}
            }
            if(! (category_name in ORGANIZED_DETAILS_LIST[legal_entity_name][division_name])){
                ORGANIZED_DETAILS_LIST[legal_entity_name][division_name][category_name] = []
            }
            ORGANIZED_DETAILS_LIST[legal_entity_name][division_name][category_name].push(
                value
            );
        }
    });
    var header_row = $("#templates .assign-unit-edit-row-header tr");
    var content_row = $("#templates .assigned-unit-edit-row tr");
    ASSIGN_UNIT_SAVE_DETAILS = {};
    LEGAL_ENTITY_UNIT_MAP = {};
    sno = 0;
    $(".assigned-unit-edit-list").empty();
    $.each(ORGANIZED_DETAILS_LIST, function(legal_entity_name, entity_value){
        $("#edit-legal-entity").show();
        ++ sno;
        var le_id = sno;
        LEGAL_ENTITY_UNIT_MAP[legal_entity_name] = [];
        var bold_text = $(".bold-text");
        var normal_text = $(".normal-text");
        $.each(entity_value, function(division_name, div_value){
            $.each(div_value, function(category_name, cat_value){
                var header_clone = header_row.clone();
                $(".edit-le-name", header_clone).text("Legal Entity :- "+legal_entity_name);
                $(".edit-div-name", header_clone).text("Division :- "+returnHyphenIfNull(division_name));
                $(".edit-category-name", header_clone).text("Category :- "+returnHyphenIfNull(category_name));
                $(".assigned-unit-edit-list").append(header_clone);
                $(".select-all-units", header_clone).addClass("le-"+le_id);
                $(".select-all-units", header_clone).click(function(){
                    activateDeactivateAllUnits(le_id, legal_entity_name);
                });
                $.each(cat_value, function(key, value){
                    
                    ASSIGN_UNIT_SAVE_DETAILS[value.unit_id] = {};              
                    $.each(value.domain_names, function(key, d_value){
                        var row_clone = content_row.clone();
                        ASSIGN_UNIT_SAVE_DETAILS[value.unit_id][d_value] = false;
                        LEGAL_ENTITY_UNIT_MAP[legal_entity_name].push("unit-"+d_value+"-"+value.unit_id); 
                        $(".select-unit", row_clone).addClass("unit-"+d_value+"-"+value.unit_id);
                        $(".unit-code", row_clone).text(value.unit_code);
                        $(".unit-name .address", row_clone).text(value.unit_name);
                        $(".unit-name .address-title", row_clone).attr("title", value.address);
                        $(".unit-name .address-title", row_clone).attr("title", value.address);
                        $(".organization-type", row_clone).empty();
                        var clone = bold_text.clone();
                        clone.text(d_value);

                        $(".organization-type", row_clone).append(clone);
                        $.each(value.org_names_list[key], function(key, org_value){
                            var clone1 = bold_text.clone();
                            clone1.text(org_value);
                            $(".organization-type", row_clone).append(clone1);
                        });

                        $(".location", row_clone).text(value.geography_name);
                        $(".assigned-unit-edit-list").append(row_clone);
                        $(".select-unit", row_clone).click(function(){
                            activateDeactivateUnit(value.unit_id, d_value);
                        });
                    });
                    
                });
            });
        });
    });
}

function activateDeactivateAllUnits(le_id, legal_entity_name){
    var unit_ids = LEGAL_ENTITY_UNIT_MAP[legal_entity_name];
    status = $(".le-"+le_id).prop("checked");
    $.each(unit_ids, function(key, value){
        classes = value.split("-");
        ASSIGN_UNIT_SAVE_DETAILS[classes[2]][classes[1]] = status;
        if(status == true || status == "true"){
            $("."+value).prop("checked", true);
        }else{
            $("."+value).prop("checked", false);
        }
    });
    updatedSelectedNoOfUnits();
}

function activateDeactivateUnit(unit_id, d_value){
    unit_status = $(".unit-"+d_value+"-"+unit_id).prop("checked");
    ASSIGN_UNIT_SAVE_DETAILS[unit_id][d_value] = unit_status;
    updatedSelectedNoOfUnits();
}

function updatedSelectedNoOfUnits(){
    var count = 0;
    $.each(ASSIGN_UNIT_SAVE_DETAILS, function(key, unit_value){
        $.each(unit_value, function(key, value){
            if(value == true || value == "true"){
                ++count;
            }
        });
    });
    $(".selected_checkbox_count").text(count);
}

function getActiveUnitDict(unit_id, domain_name){
    var legal_entity_id = null;
    
    $.each(LEGAL_ENTITY_UNIT_MAP, function(legal_entity_name, unit_ids){
        var unit_id_list = [];
        $.each(unit_ids, function(key, value){
            classes = value.split("-");
            unit_id_list.push(classes[2]);
        });
        if(unit_id_list.indexOf(unit_id) > -1){
            $.each(LEGAL_ENTITIES, function(key, value){
                if(value.legal_entity_name == legal_entity_name){
                    legal_entity_id = value.legal_entity_id;
                }
            });
        }
    });    
    return {
        "unit_id": parseInt(unit_id),
        "domain_name": domain_name,
        "legal_entity_id": legal_entity_id
    }
}

$(".save-assign-unit").click(function(){
    domain_manager_id = $("#userid").val();
    var true_count = 0;
    var active_units = []
    $.each(ASSIGN_UNIT_SAVE_DETAILS, function(unit_id, unit_value){
        $.each(unit_value, function(domain_name, value){
            if(value == true || value == "true"){
                ++true_count;
                active_units.push(
                    getActiveUnitDict(unit_id, domain_name)
                );
            }
        });
    });
    if(domain_manager_id == null || domain_manager_id == ''){
        displayMessage(message.domain_manager_required);
    }else if(true_count <= 0){
        displayMessage(message.atleast_one_unit_required);
    }else{
        callSaveAssignUnitAPI(parseInt(domain_manager_id), active_units);
    }
});

function callSaveAssignUnitAPI(domain_manager_id, unit_ids){
    function onSuccess(data) {
        displayMessage(message.assign_success);
        initialize("list");
    }
    function onFailure(error) {
        custom_alert(error);
    }
    mirror.saveAssignedUnits(CLIENT_ID, domain_manager_id, unit_ids, 
        function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

$(function(){
	initialize("list");
});
