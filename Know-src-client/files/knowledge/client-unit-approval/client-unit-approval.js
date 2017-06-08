var APPROVAL_LIST = '';
var LE_DICT = '';
var LE_ID = '';
var LE_APPROVAL_LIST = '';
var DIV_CAT_COMBINATIONS = '';
var unit_approval_details = [];

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        LE_ID = '';
        DIV_CAT_COMBINATIONS = '';
        unit_approval_details = [];
        function onSuccess(data) {
            APPROVAL_LIST = data.unit_approval_list;
            loadApprovalList();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getClientUnitApprovalList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else{
        LE_APPROVAL_LIST = '';
        function onSuccess(data) {
            LE_APPROVAL_LIST = data.entity_unit_approval_list;
            loadApprovalForm();
        }
        function onFailure(error) {
            displayMessage(error);
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

$(".submit-approval-form").click(function(){
    submitApprovalForm();
});

$(".cancel-approval-form").click(function(){
    initialize("list");
});

function loadApprovalList(){
    $(".tbody-client-unit-list").empty();
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

    if(sno == 0){
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".tbody-client-unit-list").append(clone);
    }

}
function generateDivisionCategoryCombinations(){
    DIV_CAT_COMBINATIONS = {}
    $.each(LE_APPROVAL_LIST, function(key, value){
        var division_name = value["division_name"];
        var category_name = value["category_name"];
        var class_division_name = division_name
        var class_category_name = category_name
        if(!(division_name in DIV_CAT_COMBINATIONS)){
            DIV_CAT_COMBINATIONS[division_name] = {}
        }
        if(division_name != null){
            class_division_name = division_name.replace(/ /g,'')
        }
        if(category_name != null){
            class_category_name = category_name.replace(/ /g,'')
        }
        if(!(category_name in DIV_CAT_COMBINATIONS[division_name])){
            class_name = "div-cat-"+class_division_name+"-"+class_category_name;
            DIV_CAT_COMBINATIONS[
                division_name][category_name] = class_name
        }
    });
}
function loadApprovalForm(){
    $(".tbody-approval-list").empty();
    generateDivisionCategoryCombinations();
    $(".approve_group_name").text("Group : "+LE_DICT[LE_ID]["group_name"]);
    $(".approve_country_name").text("Country : "+LE_DICT[LE_ID]["country_name"]);
    if(LE_DICT[LE_ID]["bg_name"] == null){
        $(".approve_bg_name").text("Business Group : -");
    }else{
        $(".approve_bg_name").text("Business Group : "+LE_DICT[LE_ID]["bg_name"]);
    }

    $(".approve_le_name").text("Legal Entity : "+LE_DICT[LE_ID]["le_name"]);
    $.each(LE_APPROVAL_LIST, function(key, value){
        var division_name = value["division_name"];
        var category_name = value["category_name"];
        class_name = DIV_CAT_COMBINATIONS[division_name][category_name];
        var selected_div = $(".tbody-approval-list").find("."+class_name);

        if(selected_div.length <= 0){
            var div_container = $("#templates .add-container");
            var clone = div_container.clone();
            clone.addClass(class_name);
            $(".tbody-approval-list").append(clone);
            selected_div = $(".tbody-approval-list").find("."+class_name);

            var unit_list = selected_div.find(".unit-tbody");
            var group_unit_row = $(".unit-head-template tr");
            var clone3 = group_unit_row.clone();
            $('.group-approve-control', clone3).attr('id', class_name);
            $('.group-approve-control', clone3).on('change', function () {
                updateGroupUnitStatus(this);
            });
            $(".group-reason", clone3).attr('id', 'reason-'+class_name);
            $('.group-reason', clone3).on('change', function () {
                updateGroupUnitReason(this);
            });
            unit_list.append(clone3);

            if(division_name == null) division_name = "Divison : Nil"; else  division_name = "Divison : " + division_name;
            if(category_name == null) category_name = "Category : Nil"; else category_name = "Category : " + category_name;
            selected_div.find(".division").text(division_name);
            selected_div.find(".category").text(category_name);
        }

        var unit_list = selected_div.find(".unit-tbody");
        var unit_row = $(".unit-row-template tr");
        var clone1 = unit_row.clone();
        $(".sno", clone1).attr("id", "sno-"+(key+1));
        $(".unit-location", clone1).text(value["geography_name"]);
        $(".unit-code", clone1).text(value["unit_code"]);
        $(".unit-name", clone1).text(value["unit_name"]);
        $(".address", clone1).text(value["address"]);
        $(".postal-code", clone1).text(value["postal_code"]);
        $(".domains", clone1).text(value["domain_names"]);
        $(".orgs", clone1).text(value["org_names"]);
        $(".reason", clone1).addClass("reason-"+(key+1));
        $(".reason", clone1).addClass("group-reason-"+class_name);
        var clone2 = $(".approve-drop-down select").clone();
        clone2.addClass("approval-drop-down-"+(key+1));
        clone2.addClass("group-select-"+class_name);


        $(".approve-control", clone1).html(clone2);
        unit_list.append(clone1);
        $(".approval-drop-down-"+(key+1)).change(function(){
            updateUnitStatus(this,
                "approval-drop-down-"+(key+1),
                "reason-"+(key+1)
            )
        });
    });
    var snos = $(".tbody-approval-list").find(".sno");
    var count = 1;
    $.each(snos, function(key, value){
        var sno_id = $(value).attr("id")
        $("#"+sno_id).text(count);
        ++ count;
    });
}
function updateUnitStatus(e, selectbox_class, reason_class){
    var str = $(e).attr('class').split(' ').pop();
    var c_class = str.substring(str.indexOf("div"));
    $('#'+c_class).val('0');
    var selected_option = $("."+selectbox_class).val();
    if(selected_option == 2){
        $("."+reason_class).show();
    }else{
        $("."+reason_class).hide();
        //$("."+reason_class).val('');
    }
}
function updateGroupUnitStatus(e){

    var selected_class = $(e).attr('id');
    var selected_option = $("#"+selected_class).val();
    $('.group-select-'+selected_class).each(function() {
        $('.group-select-'+selected_class).val(selected_option);
        $('.group-reason-'+selected_class).hide();
    });
    if(selected_option == 2){
        $("#reason-"+selected_class).show();
    }else{
        $("#reason-"+selected_class).hide();
    }
}
function updateGroupUnitReason(e){
    var selected_class = $(e).attr('id');
    var selected_value = $(e).val();
    $('.group-'+selected_class).each(function() {
        $('.group-'+selected_class).val(selected_value);
    });
}
function getApprovalRow(unit_id, approval_status, reason){
    if(approval_status == 1){
        approval_status = true;
    }else{
        approval_status = false;
    }
    return {
        "legal_entity_name": $(".approve_le_name").text().split(":")[1].trim(),
        "unit_id": unit_id,
        "approval_status": approval_status,
        "reason": reason
    }
}
function validateForm(){
    var result = true;
    $.each(LE_APPROVAL_LIST, function(key, value){
        var unit_id = value["unit_id"];
        var approve_drop_down_class = "approval-drop-down-"+(key+1);
        var reason_class = "reason-"+(key+1);
        var selected_option =   $("."+approve_drop_down_class).val();
        var reason = $("."+reason_class).val().trim();
        if(selected_option == 2){
            if(reason.length == 0){
                displayMessage(message.reason_required);
                result = false;
            }else if (validateMaxLength("remark", reason, "Reason") == false) {
                result = false;
            }else{
                unit_approval_details.push(
                    getApprovalRow(unit_id, selected_option, reason)
                )
            }
        }else if(selected_option == 1){
            unit_approval_details.push(
                getApprovalRow(unit_id, selected_option, "")
            )
        }
    });
    if(result == false){
        return false;
    }else{
        return true;
    }
}
function submitApprovalForm(){
    validation_result = validateForm();
    if(validation_result){
        if(unit_approval_details.length > 0){
            function onSuccess(data) {
                displaySuccessMessage(message.action_success);
                initialize("list");
            }
            function onFailure(error) {
                displayMessage(error);
            }
            mirror.approveUnit(unit_approval_details,
                function (error, response) {
                if (error == null) {
                    onSuccess(response);
                } else {
                    onFailure(error);
                }
            });
        }else{
            displayMessage(message.approve_atleast_one);
        }
    }
}
//initialization
$(function() {
    initialize("list");
    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
});
