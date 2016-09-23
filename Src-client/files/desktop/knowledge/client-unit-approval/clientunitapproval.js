var APPROVAL_LIST = ''
var LE_DICT = '';

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
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getLEUnitApprovalList(function (error, response) {
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
    var sno = 0
    var approval_row = $("#templates .table-approval-list tr");
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
        $(".bg-name", clone).text(value.business_group_name);
        $(".country-name", clone).text(value.country_name);
        $(".le-name", clone).text(value.legal_entity_name);
        $(".no-of-units", clone).text(value.unit_count);
        $(".btn-save", clone).click(function(){
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


//initialization
$(function () {
    initialize("list");
});