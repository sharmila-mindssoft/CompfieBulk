var COUNTRIES = '';
var DOMAINS = '';
var KNOWLEDGE_MANAGERS = '';
var KNOWLEDGE_EXECUTIVES = '';
var TECHNO_MANAGERS = '';
var TECHNO_EXECUTIVES = '';
var DOMAIN_MANAGERS = '';
var DOMAIN_EXECUTIVES = '';
var USER_MAPPINGS = '';

var ACTIVE_PARENT_USER = '';
var ACTIVE_CHILD_USERS = [];
var NEW_CHILD_USER_IDS = [];
var NEW_CHILD_USER_NAMES = [];
var selected_country = '';
var selected_domain = '';

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACDomain = $('#ac-domain');
var CountryVal = $('#countryval');
var Country = $('#country');
var DomainVal = $('#domainval');
var Domain = $('#domain');
var cTab = 'know-mgr-exec-tab';
var uCategory = '4';
$(".user-tab li").click(function() {
    ACCountry.hide();
    ACDomain.hide();
    activateTab($(this).attr('value'));
    cTab = $(this).attr('value');
    if(cTab == 'know-mgr-exec-tab'){
        uCategory = '4';
    }else if(cTab == 'tech-mgr-exec-tab'){
        uCategory = '6';
    }else if(cTab == 'tech-mgr-mgr-tab'){
        uCategory = '7';
    }else{
        uCategory = '8';
    }
});

$(".btn-cancel").click(function(){
    initialize();
});

$("#show").click(function(){
    if(validateFilters()){
        $(".user-grid").show();
        $(".submit-button-container").show();
        ACTIVE_PARENT_USER = '';
        ACTIVE_CHILD_USERS = [];
        NEW_CHILD_USER_IDS = [];
        NEW_CHILD_USER_NAMES = [];
        loadParentUsers();
        loadChildUsers();
    }
});

$("#save").click(function(){
    saveUserMapping();
});

function initialize(){
    clearFields();
    clearMessage();
    displayLoader();
    function onSuccess(data) {
        COUNTRIES = data.countries;
        DOMAINS = data.domains;
        KNOWLEDGE_MANAGERS = data.knowledge_managers;
        KNOWLEDGE_EXECUTIVES = data.knowledge_users;
        TECHNO_MANAGERS = data.techno_managers;
        TECHNO_EXECUTIVES = data.techno_users;
        DOMAIN_MANAGERS = data.domain_managers;
        DOMAIN_EXECUTIVES = data.domain_users;
        USER_MAPPINGS = data.user_mappings;
        //PARENT_USERS = KNOWLEDGE_MANAGERS;
        //CHILD_USERS = KNOWLEDGE_EXECUTIVES;
        activateTab(cTab);
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getUserMappings(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });  
}

function clearFields(){
    $("#country").val("");
    $("#domain").val("");
    $("#countryval").val("");
    $("#domainval").val("");
    $(".parent-user-list").empty();
    $(".child-user-list").empty();
    ACTIVE_PARENT_USER = '';
    ACTIVE_CHILD_USERS = [];
    NEW_CHILD_USER_IDS = [];
    NEW_CHILD_USER_NAMES = [];
    selected_country = '';
    selected_domain = '';
    //cTab = '';
}

function activateTab(active_class){
    clearFields();
    tabs = [
        "know-mgr-exec-tab", "tech-mgr-exec-tab",
        "tech-mgr-mgr-tab", "domain-mgr-exec-tab"
    ] 
    parent_users = [
        "Knowledge Manager", "Techno Manager", "Techno Manager",
        "Domain Manager"
    ]
    child_users = [
        "Knowledge Excecutive", "Techno Excecutive", "Domain Manager",
        "Domain Excecutive"
    ]
    parent_users_list = [
        KNOWLEDGE_MANAGERS, TECHNO_MANAGERS, TECHNO_MANAGERS, DOMAIN_MANAGERS
    ]
    child_users_list = [
        KNOWLEDGE_EXECUTIVES, TECHNO_EXECUTIVES, DOMAIN_MANAGERS, DOMAIN_EXECUTIVES
    ]
    $.each(tabs, function(key, value){
        if(value == active_class){
            //$("."+value).addClass("active");
            if(active_class == tabs[key]){
                $(".parent-user").text(parent_users[key]);
                $(".child-user").text(child_users[key]);
                PARENT_USERS = parent_users_list[key];
                CHILD_USERS = child_users_list[key];
            }
        }else{
            //$("."+value).removeClass("active");
        }
    });
    hideLoader();
}

function loadParentUsers(){
    $(".parent-user-list").empty();
    if(validateFilters() == true){
        var parent_user_row = $("#templates .drop-down-option li");
        if(PARENT_USERS.length > 0){
            $.each(PARENT_USERS, function(key, value){
                index_of_selected_country = value.country_ids.indexOf(selected_country);
                index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
                if(index_of_selected_country != -1 && index_of_selected_domain != -1){
                    var clone = parent_user_row.clone();
                    clone.html(value.employee_name + '<i></i>');
                    $(".parent-user-list").append(clone);
                    clone.click(function(){
                        activateParentUser(this, value.user_id);
                    });
                }
            });
            $("#save").show();
            if($(".parent-user-list li").length == 0){
                var clone = $("#templates .drop-down-option").clone();
                clone.html('No User(s) Found');
                $(".parent-user-list").append(clone);
                $("#save").hide();
            }
        }else{
            var clone = $("#templates .drop-down-option").clone();
            clone.html('No User(s) Found');
            $(".parent-user-list").append(clone);
            $("#save").hide();
        }
        
    }
}

function loadChildUsers(){
    $(".child-user-list").empty();
    if(validateFilters() == true){
        var child_user_row = $("#templates .drop-down-option li");
        if(CHILD_USERS.length > 0){
            $.each(CHILD_USERS, function(key, value){
                index_of_selected_country = value.country_ids.indexOf(selected_country);
                index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
                if(index_of_selected_country != -1 && index_of_selected_domain != -1 && value.is_active){
                    var clone = child_user_row.clone();
                    clone.html(value.employee_name + '<i></i>');
                    $(".child-user-list").append(clone);
                    clone.click(function(){
                        activateChildUser(this, value.user_id);
                    });
                }
            });
            $("#save").show();
            if($(".child-user-list li").length == 0){
                var clone = $("#templates .drop-down-option").clone();
                clone.html('No User(s) Found');
                $(".child-user-list").append(clone);
                $("#save").hide();
            }
        }else{
            var clone = $("#templates .drop-down-option").clone();
            clone.html('No User(s) Found');
            $(".child-user-list").append(clone);
            $("#save").hide();
        }
    }
}

function validateFilters(){
    result = true;
    selected_country = parseInt($("#country").val());
    selected_country_text = $("#countryval").val();
    selected_domain = parseInt($("#domain").val());
    selected_domain_text = $("#domainval").val();
    if(selected_country == '' || selected_country_text == ''){
        displayMessage(message.country_required);
        result = false;
    }else if(selected_domain == '' || selected_domain_text == ''){
        displayMessage(message.domain_required);
        result = false;
    }
    return result
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    var current_id = id_element[0].id;
    if(current_id == 'country'){
      DomainVal.val('');
      Domain.val('');
    }
}

//load country list in autocomplete text box
CountryVal.keyup(function(e){
    $(".parent-user-list").empty();
    $(".child-user-list").empty();
    $("#save").hide();
    var text_val = $(this).val();
    var condition_fields = ["is_active"];
    var condition_values = [true];
    commonAutoComplete(
      e, ACCountry, Country, text_val, 
      COUNTRIES, "country_name", "country_id", function (val) {
        onAutoCompleteSuccess(CountryVal, Country, val);
      }, condition_fields, condition_values);
});


//load domain list in autocomplete text box
DomainVal.keyup(function(e){
    $(".parent-user-list").empty();
    $(".child-user-list").empty();
    $("#save").hide();
    var condition_fields = ["is_active"];
    var condition_values = [true];
    if(Country.val() != ''){
      condition_fields.push("country_ids");
      condition_values.push(Country.val());
    }
    var text_val = $(this).val();
    commonAutoComplete(
      e, ACDomain, Domain, text_val, 
      DOMAINS, "domain_name", "domain_id", function (val) {
          onAutoCompleteSuccess(DomainVal, Domain, val);
      }, condition_fields, condition_values);
});


function activateParentUser(element, user_id){

    var chkstatus = $(element).attr('class');

    $('.parent-user-list li').each(function () {
        $(this).removeClass('active');
        $(this).find('i').removeClass('fa fa-check pull-right');
        ACTIVE_PARENT_USER = '';
    });

    if (chkstatus != 'active') {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');
        ACTIVE_PARENT_USER = user_id;
    }else{
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
        ACTIVE_PARENT_USER = '';
    }
    activateChildUsers();
}

function activateChildUsers(){
    ACTIVE_CHILD_USERS = [];
    NEW_CHILD_USER_IDS = [];
    NEW_CHILD_USER_NAMES = [];
    var INACTIVE_CHILD_USERS = [];

    $.each(USER_MAPPINGS, function(key, value){
        if(value.parent_user_id == ACTIVE_PARENT_USER && value.country_id == selected_country && value.domain_id == selected_domain){
            ACTIVE_CHILD_USERS.push(value.child_user_id);
        }
        else if(value.parent_user_id != ACTIVE_PARENT_USER && value.country_id == selected_country && value.domain_id == selected_domain){
            INACTIVE_CHILD_USERS.push(value.child_user_id);
        }
    });
    //if(ACTIVE_CHILD_USERS.length > 0){
    $(".child-user-list").empty();
    if(validateFilters() == true){
        var child_user_row = $("#templates .drop-down-option li");
        $.each(CHILD_USERS, function(key, value){
            index_of_selected_country = value.country_ids.indexOf(selected_country);
            index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
            //index_of_mapped_user = MAPPED_CHILD_USERS.indexOf(value.user_id);
            if(index_of_selected_country != -1 && index_of_selected_domain != -1){
                var clone = child_user_row.clone();
                clone.html(value.employee_name + '<i> </i>');
                $(".child-user-list").append(clone);
                clone.click(function(){
                    activateChildUser(this, value.user_id);
                });

                if(ACTIVE_CHILD_USERS.indexOf(value.user_id) != -1){
                    clone.addClass('active');
                    clone.find('i').addClass('fa fa-check pull-right');
                }else if(INACTIVE_CHILD_USERS.indexOf(value.user_id) != -1){
                    if(cTab != 'tech-mgr-mgr-tab'){
                        clone.remove();
                    }
                }else if(ACTIVE_CHILD_USERS.indexOf(value.user_id) == -1 && value.is_active == false){
                    clone.remove();
                }
            }
        });
        $("#save").show();
        if($(".child-user-list li").length == 0){
            var clone = $("#templates .drop-down-option").clone();
            clone.html('No User(s) Found');
            $(".child-user-list").append(clone);
            $("#save").hide();
        }
    }   
    //}
}

function activateChildUser(element, user_id){
    var chkstatus = $(element).attr('class');
    if (chkstatus == 'active'){
        displayLoader();
        if(ACTIVE_PARENT_USER != ''){
            mirror.checkUserMappings(selected_country, selected_domain,
                ACTIVE_PARENT_USER, parseInt(user_id), parseInt(uCategory), 
                function (error, response) {
                    if (error == null) {
                        $(element).removeClass('active');
                        $(element).find('i').removeClass('fa fa-check pull-right');
                        index = ACTIVE_CHILD_USERS.indexOf(user_id);
                        ACTIVE_CHILD_USERS.splice(index, 1);

                        new_index = NEW_CHILD_USER_IDS.indexOf(user_id);
                        NEW_CHILD_USER_IDS.splice(new_index, 1);

                        new_name_index = NEW_CHILD_USER_NAMES.indexOf($(element).text());
                        NEW_CHILD_USER_NAMES.splice(new_name_index, 1);

                        hideLoader();
                    } else {
                        if(error == "CannotRemoveUserTransactionExists"){
                            displayMessage(message.cant_remove_trasaction_exists);
                        }else{
                            displayMessage(error);
                        }
                        hideLoader();
                    }
            });
        }else{
            $(element).removeClass('active');
            $(element).find('i').removeClass('fa fa-check pull-right');
            index = ACTIVE_CHILD_USERS.indexOf(user_id);
            ACTIVE_CHILD_USERS.splice(index, 1);

            new_index = NEW_CHILD_USER_IDS.indexOf(user_id);
            NEW_CHILD_USER_IDS.splice(new_index, 1);

            new_name_index = NEW_CHILD_USER_NAMES.indexOf($(element).text());
            NEW_CHILD_USER_NAMES.splice(new_name_index, 1);
            hideLoader();
        }
    }else{
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');
        //index = ACTIVE_CHILD_USERS.indexOf(user_id)
        ACTIVE_CHILD_USERS.push(user_id);
        NEW_CHILD_USER_IDS.push(user_id);
        NEW_CHILD_USER_NAMES.push($(element).text())
    }
}

function validateUserMapping(){
    result = true;
    if(validateFilters() == true){
        if(ACTIVE_PARENT_USER == ''){
            displayMessage(message.parent_user_required);
            result = false;
        }else if(ACTIVE_CHILD_USERS.length == 0){
            //displayMessage(message.child_user_required);
            result = true;
        }
    }else{
        result = false;
    }
    return result;
}

function saveUserMapping(){
    displayLoader();
    if(validateUserMapping() == true){
        function onSuccess(data) {
            displaySuccessMessage(message.mapping_save_success);
            initialize();
        }
        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }
        mirror.saveUserMappings(selected_country, selected_domain,
            ACTIVE_PARENT_USER, ACTIVE_CHILD_USERS, parseInt(uCategory), NEW_CHILD_USER_IDS, 
            NEW_CHILD_USER_NAMES,  
            function (error, response) {
                if (error == null) {
                    onSuccess(response);
                } else {
                    onFailure(error);
                }
            });
    }else{
        hideLoader();
    }
}

//initialization
$(function () {
    initialize();
});