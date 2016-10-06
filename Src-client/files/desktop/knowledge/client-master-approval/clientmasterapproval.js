var COUNTRIES = '';
var GROUPS = '';
var INDUSTRIES = '';
var USERS = '';
var COUNTRIES = '';
var DOMAINS = '';
var LEGAL_ENTITIES = '';
var BUSINESS_GROUPS = '';
var DATE_CONFIGURATIONS = '';

var group_approval_details = []
var industry_id_name_map = {};
var user_id_name_map = {};
var country_id_name_map = {};
var domain_id_name_map = {};
var bg_id_name_map = {};

function initialize(){
    $(".client-group-grid").hide();
    $(".approve-group-div").hide();
    function onSuccess(data) {
        COUNTRIES = data.countries;
        GROUPS = data.group_approval_list;
    }
    function onFailure(error) {
        custom_alert(error);
    }
    mirror.getClientGroupApprovalList(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
    
}

function onCountrySuccess(val){
    $('#countryval').val(val[1]);
    $('#country-id').val(val[0]);
}

$('#countryval').keyup(function (e) {
    function callback(val) {
        onCountrySuccess(val);
    }
    var textval = $(this).val();
    getCountryAutocomplete(e, textval, COUNTRIES, callback, flag=true);
});

function onGroupSuccess(val) {
  $('#groupsval').val(val[1]);
  $('#group-id').val(val[0]);
}

$('#groupsval').keyup(function (e) {
    function callback(val) {
        onGroupSuccess(val);
    }
    var country_id = parseInt($("#country-id").val());
    var country_filtered_groups = []
    $.each(GROUPS, function(key, value){
        if(value.country_ids.indexOf(country_id) > -1){
            country_filtered_groups.push(value);
        }
    });
    var textval = $(this).val();
    getGroupAutocomplete(
        e, textval, country_filtered_groups, callback, flag=true
    );
});

$(".close").click(function(){
    closePopup();
});

$(".btn-show").click(function(){
    $(".group-list").empty();
    clearMessage();
    var country_id = parseInt($("#country-id").val());
    var group_id = parseInt($("#group-id").val());
    if(!country_id && !group_id){
        displayMessage(message.country_or_group_required)
        return false;
    }
    $(".client-group-grid").show();
    var group_row = $("#templates .group-row tr");
    var sno = 0;
    $.each(GROUPS, function(key, value){
        if(
            value.client_id == group_id ||
            value.country_ids.indexOf(country_id) > -1
        ){
            ++ sno;
            var clone = group_row.clone();
            $(".sno", clone).text(sno);
            $(".group_name a", clone).text(value.group_name);
            $(".group_name a", clone).click(function(){
                displayPopup(
                    value.client_id, value.group_name, "", value.username
                );
            });
            $(".email_id", clone).text(value.username);
            $(".le_count", clone).text(value.le_count);
            var select_box_class = "action-"+value.client_id;
            var reason_class = "reason-"+value.client_id;
            $(".action select", clone).addClass(select_box_class);
            $("."+select_box_class).val("0");
            $(".reason", clone).addClass(reason_class);
            $(".group-list").append(clone);
            $("."+select_box_class).change(function(){
                updateGroupStatus(select_box_class, reason_class)
            });
        }
    });
    if(sno > 0){
        $(".approve-group-div").show()
    }else{
        $(".approve-group-div").hide()
        var no_record_row = $("#templates .no-records tr");
        var clone = no_record_row.clone();
        $(".group-list").append(clone);
    }
});

$(".approve-group").click(function(){
    submitApprovalForm();
});

function getApprovalRow(unit_id, approval_status, reason){
    if(approval_status == 1){
        approval_status = true;
    }else{
        approval_status = false;
    }
    return {
        "client_id": unit_id,
        "approval_status": approval_status,
        "reason": reason
    }
}

function validateForm(){
    var result = true;
    var country_id = parseInt($("#country-id").val());
    var group_id = parseInt($("#group-id").val());
    $.each(GROUPS, function(key, value){
        if(
            value.client_id == group_id ||
            value.country_ids.indexOf(country_id) > -1
        ){
            var select_box_class = "action-"+value.client_id;
            var reason_class = "reason-"+value.client_id;
            var selected_option =   $("."+select_box_class).val();
            var reason = $("."+reason_class).val().replace(/ /g,'');
            if(selected_option == 2){
                if(reason.length == 0){
                    displayMessage(message.reason_required);
                    result = false;
                }else{
                    group_approval_details.push(
                        getApprovalRow(value.client_id, selected_option, reason)
                    )
                }
            }else if(selected_option == 1){
                group_approval_details.push(
                    getApprovalRow(value.client_id, selected_option, reason)
                )
            }
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
        if(group_approval_details.length > 0){
            function onSuccess(data) {
                displayMessage(message.group_approve_success);
                initialize();
            }
            function onFailure(error) {
                custom_alert(error);
            }
            mirror.approveClientGroup(group_approval_details,
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

function updateGroupStatus(select_box_class, reason_class){
    var selected_option = $("."+select_box_class).val();
    if(selected_option == 2){
        $("."+reason_class).show();    
    }else{
        $("."+reason_class).hide();   
    } 
}

function loadLegalEntities(group_name, short_name, group_admin){
    $(".client_name").text("Client Group: "+group_name);
    $(".client_short_name").text("Shortname: "+short_name);
    $(".admin_username").text("Username: "+group_admin);
    $(".overlay .tbody-le").empty();
    var le_row = $("#templates .le-row .le");
    var domain_header = $("#templates .domain-header");
    var domain_body = $("#templates .tbody-domain");
    var domain_row = $("#templates .domain-row tr");
    $.each(LEGAL_ENTITIES, function(key, value){
        var clone = le_row.clone();
        var clone1 = domain_header.clone();
        var clone2 = domain_body.clone();
        $(".le_country", clone).text("Country: "+country_id_name_map[value.c_id]);
        $(".le_bg", clone).text("Business Group: -");
        if(value.b_g != null){
            $(".le_bg", clone).text("Business Group: "+value.b_g.bg_name);    
        }
        $(".le_name", clone).text("Legal Entity: "+value.l_e_name);
        var incharge_persons = ""
        $.each(value.inc_p, function(key, value){
            if(key == 0) {
                incharge_persons += user_id_name_map[value]
            }else{
                incharge_persons += ", "+user_id_name_map[value]
            }
        });
        $(".incharge_person", clone).text("Incharge Person: "+incharge_persons);
        $(".logo img", clone).attr(
            "src","http://"+window.location.host+"/knowledge/clientlogo/"+value.logo);
        $(".file_space", clone).text("File space: "+value.f_s);
        $(".contract_from", clone).text("Contract From: "+value.c_f);
        $(".contract_to", clone).text("Contract To: "+value.c_t);
        $(".total_licence", clone).text("Total Licence(s): "+value.n_o_l);
        $("tbody-domain", clone).append(clone2);
        $(".overlay .tbody-le").append(clone);
        $(".overlay .tbody-le").append(clone1);
        $.each(value.d, function(key, d_val){
            $.each(d_val.org, function(key, org_val){
                var clone2 = domain_row.clone();
                $(".domain-name", clone2).text(domain_id_name_map[d_val.d_id]);
                $(".org-name", clone2).text(industry_id_name_map[parseInt(key)]);
                $(".no-of-units", clone2).text(org_val);
                $(".tbody-domain", clone1).append(clone2);
            });
        });
        
    });
}

function closePopup(){
    $('.overlay').css('visibility', 'hidden');
    $('.overlay').css('opacity', '0');
}

function generateIdNameMaps(){
    $.each(INDUSTRIES, function(key, value){
        industry_id_name_map[value.industry_id] = value.industry_name;
    });
    $.each(USERS, function(key, value){
        user_id_name_map[value.user_id] = value.employee_name;
    });
    $.each(COUNTRIES, function(key, value){
        country_id_name_map[value.country_id] = value.country_name;
    });
    $.each(DOMAINS, function(key, value){
        domain_id_name_map[value.domain_id] = value.domain_name;
    });
    $.each(BUSINESS_GROUPS, function(key, value){
        bg_id_name_map[value.business_group_id] = value.business_group_name;
    });
}

function loadDateConfigurations(){
    var date_config_row = $("#templates .date-config-row tr");
    $(".date-configuration-rows").empty();
    $.each(DATE_CONFIGURATIONS, function(key, value){
        var clone = date_config_row.clone();
        $(".dconfig-country_name", clone).text(country_id_name_map[value.country_id]);
        $(".dconfig-domain-name", clone).text(domain_id_name_map[value.domain_id]);
        $(".dconfig-from", clone).text(getMonth_IntegertoString(value.period_from));
        $(".dconfig-to", clone).text(getMonth_IntegertoString(value.period_to));
        $(".date-configuration-rows").append(clone);
    });
}

function displayPopup(client_id, group_name, short_name, group_admin) {
    $('.overlay').css('visibility', 'visible');
    $('.overlay').css('opacity', '1');
    function onSuccess(data) {
        INDUSTRIES = data.industries;
        USERS = data.users;
        COUNTRIES = data.countries;
        DOMAINS = data.domains;
        LEGAL_ENTITIES = data.legal_entities;
        BUSINESS_GROUPS = data.business_groups;
        DATE_CONFIGURATIONS = data.date_configurations;
        generateIdNameMaps();
        loadLegalEntities(group_name, short_name, group_admin);
        loadDateConfigurations();
    }
    function onFailure(error) {
        custom_alert(error);
    }
    mirror.getEditClientGroupFormData(parseInt(client_id),
        function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}


//initialization
$(function () {
    initialize();
});