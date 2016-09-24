var APPROVAL_LIST = '';
var LE_DICT = '';
var LE_ID = '';
var LE_APPROVAL_LIST = '';
var DIV_CAT_COMBINATIONS = '';

function initialize(type_of_form){
    showPage(type_of_form);
    if(type_of_form == "list"){
        function onSuccess(data) {
            APPROVAL_LIST = data.unit_approval_list;  
            loadApprovalList();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getClientUnitApprovalList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else{
        function onSuccess(data) {
            LE_APPROVAL_LIST = data.entity_unit_approval_list;
            loadApprovalForm();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getEntityApprovalList(LE_ID, function (error, response) {
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
        $("#client-unit-approve-view").show();
        $("#clientunit-approve").hide();
    }else{
        $("#client-unit-approve-view").hide();
        $("#clientunit-approve").show();
    }
}

function loadApprovalList(){
    var sno = 0;
    var approval_row = $("#templates .table-approval-list tr");
    LE_DICT = {};
    $.each(APPROVAL_LIST, function(key, value){
        ++sno;
        var clone = approval_row.clone();
        var business_group_name = value.business_group_name
        if(business_group_name == null){
            business_group_name = "-";
        }
        var legal_entity_id = value.legal_entity_id;
        $(".sno", clone).text(sno);
        $(".group-name", clone).text(value.group_name);
        $(".bg-name", clone).text(business_group_name);
        $(".country-name", clone).text(value.country_name);
        $(".le-name", clone).text(value.legal_entity_name);
        $(".no-of-units", clone).text(value.unit_count);
        $(".btn-save", clone).attr("id", legal_entity_id);
        $(".btn-save", clone).click(function(){
            LE_ID = parseInt($(this).attr("id"));
            initialize("approval_form");
        });
        $(".tbody-client-unit-list").append(clone);
        LE_DICT[legal_entity_id] = {
            "group_name": value.group_name,
            "bg_name": value.business_group_name,
            "country_name": value.country_name,
            "le_name": value.legal_entity_name,
        }
    });
}

function generateDivisionCategoryCombinations(){
    DIV_CAT_COMBINATIONS = {}
    $.each(LE_APPROVAL_LIST, function(value){
        division_name = value["division_name"];
        category_name = value["category_name"];
        if(!(division_name in DIV_CAT_COMBINATIONS)){
            DIV_CAT_COMBINATIONS[division_name] = {}
        }
        if(!(category_name in DIV_CAT_COMBINATIONS[division_name])){
            class_name = "div-cat-"+division_name+"-"+category_name
            DIV_CAT_COMBINATIONS[
                division_name][category_name] = class_name
        }
    });
}

function loadApprovalForm(){
    generateDivisionCategoryCombinations();
    $(".approve_group_name").text("Group:"+LE_DICT[LE_ID]["group_name"]);
    $(".approve_country_name").text("Country:"+LE_DICT[LE_ID]["country_name"]);
    $(".approve_bg_name").text("Business Group:"+LE_DICT[LE_ID]["bg_name"]);
    $(".approve_le_name").text("Legal Entity:"+LE_DICT[LE_ID]["le_name"]);
    $.each(LE_APPROVAL_LIST, function(value){
        var div_container = $("#templates .add-container");
        var clone = div_container.clone();
        $(".tbody-approval-list").append(clone);
    });
}

//initialization
$(function () {
    initialize("list");
});