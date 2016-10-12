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
var selected_country = '';
var selected_domain = '';

$(".know-mgr-exec-tab").click(function() {
    activateTab("know-mgr-exec-tab");
});
$(".tech-mgr-exec-tab").click(function() {
    activateTab("tech-mgr-exec-tab");
});
$(".tech-mgr-mgr-tab").click(function() {
    activateTab("tech-mgr-mgr-tab");
});
$(".domain-mgr-exec-tab").click(function() {
    activateTab("domain-mgr-exec-tab");
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
    activateTab("know-mgr-exec-tab");
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
        PARENT_USERS = KNOWLEDGE_MANAGERS;
        CHILD_USERS = KNOWLEDGE_EXECUTIVES;
    }
    function onFailure(error) {
        custom_alert(error);
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
    selected_country = '';
    selected_domain = '';
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
            $("."+value).addClass("active");
            if(active_class == tabs[key]){
                $(".parent-user").text(parent_users[key]);
                $(".child-user").text(child_users[key]);
                PARENT_USERS = parent_users_list[key];
                CHILD_USERS = child_users_list[key];
            }
        }else{
            $("."+value).removeClass("active");
        }
    });
}

function loadParentUsers(){
    $(".parent-user-list").empty();
    if(validateFilters() == true){
        var parent_user_row = $("#templates .drop-down-option li");
        $.each(PARENT_USERS, function(key, value){
            index_of_selected_country = value.country_ids.indexOf(selected_country);
            index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
            if(index_of_selected_country != -1 && index_of_selected_domain != -1){
                var clone = parent_user_row.clone();
                clone.text(value.employee_name);
                $(".parent-user-list").append(clone);
                clone.click(function(){
                    activateParentUser(this, value.user_id);
                });
            }
        });
    }
    
}

function loadChildUsers(){
    $(".child-user-list").empty();
    if(validateFilters() == true){
        var child_user_row = $("#templates .drop-down-option li");
        $.each(CHILD_USERS, function(key, value){
            index_of_selected_country = value.country_ids.indexOf(selected_country);
            index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
            if(index_of_selected_country != -1 && index_of_selected_domain != -1){
                var clone = child_user_row.clone();
                clone.text(value.employee_name);
                $(".child-user-list").append(clone);
                clone.click(function(){
                    activateChildUser(this, value.user_id);
                });
            }
        });
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

//retrive country autocomplete value
function onCountrySuccess(val) {
  $('#countryval').val(val[1]);
  $('#country').val(val[0]);
}
//load country list in autocomplete text box  
$('#countryval').keyup(function (e) {
  function callback(val) {
    onCountrySuccess(val);
  }
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, COUNTRIES, callback, flag = true);
});

//retrive domain autocomplete value
function onDomainSuccess(val) {
  $('#domainval').val(val[1]);
  $('#domain').val(val[0]);
}
//load country list in autocomplete text box  
$('#domainval').keyup(function (e) {
  function callback(val) {
    onDomainSuccess(val);
  }
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, DOMAINS, callback, flag = true);
});

function activateParentUser(element, user_id){
    var chkstatus = $(element).attr('class');
    if (chkstatus == 'active') {
        $(element).removeClass('active');
    }else{
        $(element).addClass('active');
    }
    ACTIVE_PARENT_USER = user_id;
    activateChildUsers();
}

function activateChildUsers(){
    ACTIVE_CHILD_USERS = [];
    $.each(USER_MAPPINGS, function(key, value){
        if(value.parent_user_id == ACTIVE_PARENT_USER){
            ACTIVE_CHILD_USERS.push(value.child_user_id);
        }
    });
    if(ACTIVE_CHILD_USERS.length > 0){
        $(".child-user-list").empty();
        if(validateFilters() == true){
            var child_user_row = $("#templates .drop-down-option li");
            $.each(CHILD_USERS, function(key, value){
                index_of_selected_country = value.country_ids.indexOf(selected_country);
                index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
                if(index_of_selected_country != -1 && index_of_selected_domain != -1){
                    var clone = child_user_row.clone();
                    clone.text(value.employee_name);
                    $(".child-user-list").append(clone);
                    clone.click(function(){
                        activateChildUser(this, value.user_id);
                    });
                    if(ACTIVE_CHILD_USERS.indexOf(value.user_id) != -1){
                        clone.addClass('active');
                    }
                }
            });
        }   
    }
    
}

function activateChildUser(element, user_id){
    var chkstatus = $(element).attr('class');
    if (chkstatus == 'active'){
        $(element).removeClass('active');
        ACTIVE_CHILD_USERS.splice(index, 1);
    }else{
        $(element).addClass('active');
        index = ACTIVE_CHILD_USERS.indexOf(user_id)
        ACTIVE_CHILD_USERS.push(user_id);
    }
}

function validateUserMapping(){
    result = true;
    if(validateFilters() == true){
        if(ACTIVE_PARENT_USER == ''){
            displayMessage(message.parent_user_required);
            result = false;
        }else if(ACTIVE_CHILD_USERS.length == 0){
            displayMessage(message.child_user_required);
            result = false;
        }
    }else{
        result = false;
    }
    return result;
}

function saveUserMapping(){
    if(validateUserMapping() == true){
        function onSuccess(data) {
            displayMessage(message.mapping_save_success);
            initialize();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveUserMappings(selected_country, selected_domain,
            ACTIVE_PARENT_USER, ACTIVE_CHILD_USERS,
            function (error, response) {
                if (error == null) {
                    onSuccess(response);
                } else {
                    onFailure(error);
                }
            });
    }
}


//initialization
$(function () {
    initialize();
});