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
var ASSIGN_UNIT_SAVE_DETAILS = [];
var LEGAL_ENTITY_UNIT_MAP = {};
var USER_CAREGORY ='';
var MAPPED_DOMAIN_USERS = {};

// auto complete - country
var manager_id = $('#userid');
var manager_name = $("#assinee");
var AcUser = $('#ac-user');

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

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
    ASSIGN_UNIT_SAVE_DETAILS = [];
    LEGAL_ENTITY_UNIT_MAP = {};
    $("#businessgroupsval").val("");
    $("#businessgroupid").val("");
    $("#legalentityval").val("");
    $("#legalentityid").val("");
    $("#assinee").val("");
    $("#userid").val("");
    $("#ac-user").hide();
    $(".unassign-list").empty();
    $(".assigned-list").empty();
    $(".assigned-unit-view-list").empty();
    $(".assigned-unit-edit-list").empty();
    $("#edit-legal-entity").hide();
}

//Finds the mode of page and gets the records from DB through api
function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();

    // Initial Page of all the unassigned units total grouped by domain wise
    if(type_of_form == "list"){
        clearForm();
        function onSuccess_list(data) {
            UNASSIGNED_UNITS = data["unassigned_units_list"];
            if(data["user_category_id"] == 5){
                USER_CAREGORY = "Domain Manager";
            }else{
                USER_CAREGORY = "Domain Executive";
            }
            loadUnAssignedUnitsList();
            hideLoader();
        }
        function onFailure_list(error) {
            displayMessage(error);
        }
        displayLoader();
        mirror.getUnassignedUnitsList(function (error, response) {
            if (error == null) {
                onSuccess_list(response);
            } else {
                onFailure_list(error);
                hideLoader();
            }
        });
    }else if(type_of_form == "assign"){
        function onSuccess_assign(data) {
            BUSINESS_GROUPS = data.business_groups;
            ASSIGNED_UNIT_DETAILS_LIST = data.assigned_unit_details_list;
            DOMAIN_MANAGER_USERS = data.domain_manager_users;
            LEGAL_ENTITIES = data.unit_legal_entity;
            MAPPED_DOMAIN_USERS = data.mapped_domain_users;
            loadAssignUnitForm();
            hideLoader();
        }
        function onFailure_assign(error) {
            displayMessage(error);
        }
        //Arguments passed to get the units yet to be assigned
        displayLoader();
        mirror.getAssignUnitFormData(
            DOMAIN_ID, CLIENT_ID, LEGAL_ENTITY_ID, function (error, response) {
            if (error == null) {
                onSuccess_assign(response);
            } else {
                onFailure_assign(error);
                hideLoader();
            }
        });
    }else if(type_of_form == "view"){
        function onSuccess_view(data) {
            ASSIGNED_UNITS = data["assigned_units_list"];
            loadAssignedUnitsList();
            hideLoader();
        }
        function onFailure_view(error) {
            displayMessage(error);
        }
        //Arguments passed to get the units assigned to corresponding executive
        displayLoader();
        mirror.getAssignedUnitsList(
            DOMAIN_ID, CLIENT_ID, LEGAL_ENTITY_ID, function (error, response) {
            if (error == null) {
                onSuccess_view(response);
            } else {
                hideLoader();
                onFailure_view(error);
            }
        });
    }else if(type_of_form == "view-details"){
        function onSuccess_details(data) {
            ASSIGNED_UNIT_DETAILS_LIST = data.assigned_unit_details_list
            loadAssignedUnitsDetailsList();
            hideLoader();
        }
        function onFailure_details(error) {
            displayMessage(error);
        }
        //Arguments passed to get the corresponding executives addigned units list and details
        displayLoader();
        mirror.getAssignedUnitDetails(
            LEGAL_ENTITY_ID, DOMAIN_MANAGER_ID, CLIENT_ID, DOMAIN_ID, function (error, response) {
            if (error == null) {
                onSuccess_details(response);
            } else {
                hideLoader();
                onFailure_details(error);
            }
        });
    }
}

//Get the type of form and loads the corresponding page
function showPage(type_of_form){
    if(type_of_form == "list"){
        $("#unassigned_units").show();
        $("#assigned_units").hide();
        $("#assign").hide();
        $("#view-details").hide();
        $('.input-sm').val('');
    }else if(type_of_form == "assign"){
        $("#unassigned_units").hide();
        $("#assigned_units").hide();
        $("#assign").show();
        $("#view-details").hide();
        $('.selected_checkbox_count').text('');
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

// To cancel an page - view unit details page
$(".cancel-view-details").click(function(){
    initialize("view");
});

// To go back to the main list page
$(".btn-back").click(function(){
    initialize("list");
});

//To cancel the assigned unit page and view the main list
$(".cancel-assign-unit").click(function(){
    initialize("list");
});

// Binds the main list page - domain wise units with total and not assigned units
function loadUnAssignedUnitsList(){
    $(".unassign-list").empty();
    $(".category_title").text(USER_CAREGORY);
    var row = $("#templates .unassign-row tr");
    var sno = 0;
    if(UNASSIGNED_UNITS.length > 0){
        $.each(UNASSIGNED_UNITS, function(key, value){
            ++sno;
            var clone = row.clone();
            $(".sno", clone).text(sno);
            $(".domain-name", clone).text(value.domain_name);
            $(".group-name", clone).text(value.group_name);
            $(".business-group-name", clone).text(returnHyphenIfNull(value.business_group_name));
            $(".legal-entity-name", clone).text(returnHyphenIfNull(value.legal_entity_name));
            $(".unassigned-units", clone).text(value.unassigned_units);
            if(value.unassigned_units.split("/")[0] == 0){
                $(".assign", clone).hide();
            }else{
                $(".assign", clone).show();
                $(".assign", clone).click(function(){
                    viewAssignUnitsForm(
                        value.domain_id, value.client_id,
                        value.domain_name, value.group_name,
                        value.business_group_name, value.legal_entity_name,
                        value.legal_entity_id
                    );
                });
            }
            if(value.unassigned_units.split("/")[0].trim() == value.unassigned_units.split("/")[1].trim()){
                $(".view", clone).hide();
            }
            else{
                $(".view", clone).show();
                $(".view", clone).click(function(){
                    viewDomainManagers(
                        value.domain_id, value.client_id,
                        value.domain_name, value.group_name,
                        value.legal_entity_id
                    );
                });
            }

            $(".unassign-list").append(clone);
        });
    }
    else{
        $('.unassign-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.unassign-list').append(clone4);
    }

}

// To navigate to the assign units page
function viewAssignUnitsForm(domain_id, client_id, domain_name, group_name, business_group_name, legal_entity_name, legal_entity_id){
    DOMAIN_ID = domain_id;
    CLIENT_ID = client_id;
    DOMAIN_NAME = domain_name;
    GROUP_NAME = group_name;
    BUSINESS_GROUP_NAME = business_group_name;
    LEGAL_ENTITY_NAME = legal_entity_name;
    LEGAL_ENTITY_ID = legal_entity_id;
    initialize("assign");
}

// To view the executives assigned with the no. of units
function viewDomainManagers(domain_id, client_id, domain_name, group_name, legal_entity_id){
    DOMAIN_ID = domain_id;
    CLIENT_ID = client_id;
    DOMAIN_NAME = domain_name;
    GROUP_NAME = group_name;
    LEGAL_ENTITY_ID = legal_entity_id;
    initialize("view");
}

// Binds the records from DB - corresponding executives with the no of units assigned
function loadAssignedUnitsList(){
    $('#domain_usr').attr("placeholder",USER_CAREGORY);
    $(".assigned-list").empty();
    var row = $("#templates .assigned-row tr");
    var sno = 0;
    $.each(ASSIGNED_UNITS, function(key, value){
        ++sno;
        var clone = row.clone();
        $(".sno", clone).text();
        $(".domain-manager", clone).text(value.employee_name);
        $(".domain-name", clone).text(DOMAIN_NAME);
        $(".group-name", clone).text(GROUP_NAME);
        $(".business-group-name", clone).text(value.business_group_name);
        $(".legal-entity-name", clone).text(value.legal_entity_name);
        $(".no-of-units", clone).text(value.unit_count);
        $(".view", clone).click(function(){
            viewAssignedUnitDetails(
                value.business_group_name, value.legal_entity_name,
                value.legal_entity_id, value.user_id, value.client_id,
                value.domain_id
            );
        });
        $(".assigned-list").append(clone);
    });
}

// To view the Assigned units list and details under a corresponding executive
function viewAssignedUnitDetails(
    business_group_name, legal_entity_name,
    legal_entity_id, user_id, client_id, domain_id
){
    BUSINESS_GROUP_NAME = business_group_name;
    LEGAL_ENTITY_NAME = legal_entity_name;
    LEGAL_ENTITY_ID = legal_entity_id;
    DOMAIN_MANAGER_ID = user_id
    DOMAIN_ID = domain_id;
    CLIENT_ID = client_id;
    initialize("view-details")
}

// Bind the records from DB - Units list and details to be assigned
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
                    var unit_ctrl = "<i class='zmdi zmdi-info address-title' data-toggle='tooltip' title='"+value.address+"'></i>&nbsp;&nbsp;"+value.unit_name;
                    $(".unit-name", row_clone).append($.parseHTML(unit_ctrl));

                    /*$(".unit-name .address", row_clone).text(value.unit_name);
                    $(".unit-name .address-title", row_clone).attr("title", value.address);
                    $(".unit-name .address-title", row_clone).attr("title", value.address);*/
                    $(".organization-type", row_clone).empty();

                    if(value.domain_names.length == 1){
                        var clone = null;
                        if(value.domain_names.indexOf(",") < 0){
                            clone = "<strong>"+value.domain_names+"</strong><br/>";
                        }
                        else{
                            clone = getCommaSeparated("domain",value.domain_names[0]);
                        }
                        $(".organization-type", row_clone).append($.parseHTML(clone));
                    }
                    else{
                        var d_names =""
                        $.each(value.domain_names, function(key, d_value){
                            if($(".organization-type")[key].innerText.indexOf(d_value) < 0){
                                var clone = "<strong>"+d_value+"</strong><br/>";
                                $(".organization-type", row_clone).append($.parseHTML(clone));
                            }
                        });
                    }
                    if(value.org_names_list[0].length == 1){
                        var clone = null;
                        if(value.org_names_list[0].indexOf(",") < 0){
                            clone = value.org_names_list[0]+"<br/>";
                        }
                        else{
                            clone = getCommaSeparated("orgn",value.org_names_list[0]);
                        }
                        $(".organization-type", row_clone).append($.parseHTML(clone));
                    }
                    else{
                        var clone = null;
                        clone = getArrayvalues(value.org_names_list[0]);
                        $(".organization-type", row_clone).append($.parseHTML(clone));
                    }
                    $(".location", row_clone).text(value.geography_name);
                    $(".assigned-unit-view-list").append(row_clone);

                });
            });
        });
    });
}

// To return hyphen if any value with null
function returnHyphenIfNull(value){
    if(value == null || value == "null" || value == "---"){
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

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}
//load legalentity form list in autocomplete text box
$('#assinee').keyup(function (e) {
    var textval = $(this).val();
    legal_entity_id = LEGAL_ENTITY_ID;
    var domain_users = [];

    if(ASSIGN_UNIT_SAVE_DETAILS.length > 0){
    for(var i=0;i<MAPPED_DOMAIN_USERS.length;i++){
        if(MAPPED_DOMAIN_USERS[i].legal_entity_id == legal_entity_id){
            for(var j=0;j<DOMAIN_MANAGER_USERS.length;j++){
                if(MAPPED_DOMAIN_USERS[i].user_id == DOMAIN_MANAGER_USERS[j].user_id){
                    var occur = -1;
                    for(var k=0;k<domain_users.length;k++){
                        if(domain_users[k].user_id == DOMAIN_MANAGER_USERS[j].user_id){
                            occur = 1;
                            break;
                        }
                    }
                    if(occur < 0){
                        domain_users.push({
                            "user_id":DOMAIN_MANAGER_USERS[j].user_id,
                            "employee_name":DOMAIN_MANAGER_USERS[j].employee_name,
                            "is_active":DOMAIN_MANAGER_USERS[j].is_active,
                            "user_category_id":DOMAIN_MANAGER_USERS[j].user_category_id
                        });
                        occur = -1;
                    }
                }
            }
        }
      }
      commonAutoComplete(
      e, AcUser, manager_id, textval,
      domain_users, "employee_name", "user_id", function (val) {
          onAutoCompleteSuccess(manager_name, manager_id, val);
      });
    }
});

// To load the units assigned list
function loadAssignUnitForm(){
    $(".edit-group-name").text(GROUP_NAME);
    $(".edit-domain-name").text(DOMAIN_NAME);
    $(".edit-business-grp-name").text(returnHyphenIfNull(BUSINESS_GROUP_NAME));
    $(".edit-legal-entity-name").text(returnHyphenIfNull(LEGAL_ENTITY_NAME));
    loadEditAssignedUnitsDetailsList();
}

// Not in usage
$(".show-units").click(function(){
    LEGAL_ENTITY_NAME = $("#legalentityval").val();
    LEGAL_ENTITY_ID = $('#legalentityid').val();
    BUSINESS_GROUP_NAME = $("#businessgroupsval").val();
    BUSINESS_GROUP_ID = $("#businessgroupid").val();
    if(LEGAL_ENTITY_ID == ''){
        displayMessage(message.legalentity_required)
    }
    else
    {
        loadEditAssignedUnitsDetailsList();
    }
});

// Loads the units to be assigned
function loadEditAssignedUnitsDetailsList(){
    ORGANIZED_DETAILS_LIST = {}

    $.each(ASSIGNED_UNIT_DETAILS_LIST, function(key, value){
        var legal_entity_name = value["legal_entity_name"];
        var division_name = returnHyphenIfNull(value["division_name"]);
        var category_name = returnHyphenIfNull(value["category_name"]);
        var validation_status = true;
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
    ASSIGN_UNIT_SAVE_DETAILS = [];
    LEGAL_ENTITY_UNIT_MAP = {};
    sno = 0;
    $(".assigned-unit-edit-list").empty();
    $.each(ORGANIZED_DETAILS_LIST, function(legal_entity_name, entity_value){
        $("#edit-legal-entity").show();

        var bold_text = $(".bold-text");
        var normal_text = $(".normal-text");
        $.each(entity_value, function(division_name, div_value){
            $.each(div_value, function(category_name, cat_value){
                ++ sno;
                var le_id = sno;
                var header_clone = header_row.clone();
                $(".edit-le-name", header_clone).append($.parseHTML("<strong>Legal Entity :- "+legal_entity_name+"</strong>"));
                $(".edit-div-name", header_clone).append($.parseHTML("<strong>Division :- "+returnHyphenIfNull(division_name)+"</strong>"));
                $(".edit-category-name", header_clone).append($.parseHTML("<strong>Category :- "+returnHyphenIfNull(category_name)+"</strong>"));
                $(".assigned-unit-edit-list").append(header_clone);
                $(".select-all-units", header_clone).addClass("le-"+le_id);
                $("#select-all-box", header_clone).addClass("select-all-box-le-"+le_id);
                $("#lbl-select-all", header_clone).attr('for',"select-all-box-le-"+le_id);
                $('.select-all-units le-'+le_id).prop("checked", false);
                $(".select-all-units", header_clone).click(function(){
                    activateDeactivateAllUnits(this,legal_entity_name, division_name, category_name);
                });
                if(! (legal_entity_name in LEGAL_ENTITY_UNIT_MAP)){
                    LEGAL_ENTITY_UNIT_MAP[legal_entity_name] = {}
                }
                if(! (division_name in LEGAL_ENTITY_UNIT_MAP[legal_entity_name])){
                    LEGAL_ENTITY_UNIT_MAP[legal_entity_name][division_name] = {}
                }
                if(! (category_name in LEGAL_ENTITY_UNIT_MAP[legal_entity_name][division_name])){
                    LEGAL_ENTITY_UNIT_MAP[legal_entity_name][division_name][category_name] = []
                }


                $.each(cat_value, function(key, value){
                    var data = LEGAL_ENTITY_UNIT_MAP[legal_entity_name][division_name][category_name];
                    var occur = 0;
                    for(var i=0;i<data.length;i++){
                        if(value.unit_id == data[i])
                        {
                            occur++;
                        }
                    }
                    if(occur==0){
                        LEGAL_ENTITY_UNIT_MAP[legal_entity_name][division_name][category_name].push(value.unit_id);
                        var row_clone = content_row.clone();
                        $(".select-unit", row_clone).addClass("unit-"+value.unit_id);
                        $(".unit-code", row_clone).text(value.unit_code);
                        var unit_ctrl = "<i class='zmdi zmdi-info address-title' data-toggle='tooltip' title='"+value.address+"'></i>&nbsp;&nbsp;"+value.unit_name;
                        $(".unit-name", row_clone).append($.parseHTML(unit_ctrl));
                        $(".organization-type", row_clone).empty();

                        if(value.domain_names.length == 1){
                            var clone = null;
                            if(value.domain_names.indexOf(",") < 0){
                                clone = "<strong>"+value.domain_names+"</strong><br/>";
                            }
                            else{
                                clone = getCommaSeparated("domain",value.domain_names[0]);
                            }
                            $(".organization-type", row_clone).append($.parseHTML(clone));
                        }
                        else{
                            var d_names =""
                            $.each(value.domain_names, function(key, d_value){
                                if($(".organization-type")[key].innerText.indexOf(d_value) < 0){
                                    var clone = "<strong>"+d_value+"</strong><br/>";
                                    $(".organization-type", row_clone).append($.parseHTML(clone));
                                }
                            });
                        }
                        if(value.org_names_list[0].length == 1){
                            var clone = null;
                            if(value.org_names_list[0].indexOf(",") < 0){
                                clone = value.org_names_list[0]+"<br/>";
                            }
                            else{
                                clone = getCommaSeparated("orgn",value.org_names_list[0]);
                            }
                            $(".organization-type", row_clone).append($.parseHTML(clone));
                        }
                        else{
                            var clone = null;
                            clone = getArrayvalues(value.org_names_list[0]);
                            $(".organization-type", row_clone).append($.parseHTML(clone));
                        }
                        $(".location", row_clone).text(value.geography_name);
                        $(".assigned-unit-edit-list").append(row_clone);
                        $(".select-unit", row_clone).click(function(){
                            activateDeactivateUnit(value.unit_id, le_id, data);
                        });
                    }
                });
            });
        });
    });
}

// To return comma separated domain names and organization names
function getCommaSeparated(type, value){
    var returnString = null;
    if(type == "domain"){
        split_comma = value.split(",");
        for(var i=0;i<split_comma.length;i++){
            if(returnString == ""){
                returnString = "<strong>"+split_comma[i]+"<strong><br/>";
            }
            else
                if(returnString.indexOf(split_comma[i]) < 0){
                    returnString = returnString + "<strong>"+split_comma[i]+"<strong><br/>";
                }
        }
    }
    else if(type == "orgn"){
        split_comma = value.split(",");
        for(var i=0;i<split_comma.length;i++){
            if(returnString == ""){
                returnString = split_comma[i]+"<br/>";
            }
            else
                if(returnString.indexOf(split_comma[i]) < 0){
                    returnString = returnString + split_comma[i]+"<br/>";
                }
        }
    }
    return returnString;
}

// To get the values in a string format
function getArrayvalues(arr_values){
    var returnString = "";
    for(var i=0;i<arr_values.length;i++){
        if(returnString == ""){
            returnString = arr_values[i]+"<br/>";
        }
        else
            if(returnString.indexOf(arr_values[i]) < 0){
                returnString = returnString + arr_values[i]+"<br/>";
            }
    }
    return returnString;
}

// To activate the all check box and stores in an array
function activateDeactivateAllUnits(e, legal_entity_name, division_name, category_name){
    if (e.checked) {
        var unit_ids = LEGAL_ENTITY_UNIT_MAP[legal_entity_name][division_name][category_name];
        $.each(unit_ids, function(key, value){
            $('.unit-'+value).prop('checked',true);
            updateUnitsToArray(value, "push");
        });
    } else {
        var unit_ids = LEGAL_ENTITY_UNIT_MAP[legal_entity_name][division_name][category_name];
        $.each(unit_ids, function(key, value){
            $('.unit-'+value).prop('checked',false);
            updateUnitsToArray(value, "pull");
        });
    }
    //updatedSelectedNoOfUnits();
}

// To activate particular check box checked and stores in an array
function activateDeactivateUnit(unit_id, le_id, data){
    unit_status = $(".unit-"+unit_id).prop("checked");
    var tot_chk_cnt = 0;
    if(unit_status == "true" || unit_status == true){
        updateUnitsToArray(unit_id, "push");
    }
    else if(unit_status == "false" || unit_status == false){
        $('.le-'+le_id).prop('checked',false);
        updateUnitsToArray(unit_id, "pull");
    }

    $.each(data, function(key, value){
        chk_status = $('.unit-'+value).prop('checked');
        if (chk_status == true)
        	tot_chk_cnt++;
    });

    if(data.length == tot_chk_cnt)
    	$('.le-'+le_id).prop('checked',true);
    else
    	$('.le-'+le_id).prop('checked',false);
}

// To update the checkbox units selected and stores/ removes from array
function updateUnitsToArray(unit_id, type){
    if(type == "push"){
        for(var i = ASSIGN_UNIT_SAVE_DETAILS.length - 1; i >= 0; i--) {
            if(ASSIGN_UNIT_SAVE_DETAILS[i] === unit_id) {
               ASSIGN_UNIT_SAVE_DETAILS.splice(i, 1);
            }
        }
        ASSIGN_UNIT_SAVE_DETAILS.push(unit_id);
        $(".selected_checkbox_count").text(ASSIGN_UNIT_SAVE_DETAILS.length);
    }
    else if(type == "pull"){
        for(var i = ASSIGN_UNIT_SAVE_DETAILS.length - 1; i >= 0; i--) {
            if(ASSIGN_UNIT_SAVE_DETAILS[i] === unit_id) {
               ASSIGN_UNIT_SAVE_DETAILS.splice(i, 1);
            }
        }
        $(".selected_checkbox_count").text(ASSIGN_UNIT_SAVE_DETAILS.length);
    }
}
// To store the checkbox unit selected
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

// To get the units selected to be assigned and forms a dict
function getActiveUnitDict(unit_id, domain_name){
    var legal_entity_id = null;

    for(var i=0;i<ASSIGNED_UNIT_DETAILS_LIST.length;i++){
        if(ASSIGNED_UNIT_DETAILS_LIST[i].unit_id == unit_id){
            $.each(LEGAL_ENTITIES, function(key, value){
                if(value.legal_entity_name == ASSIGNED_UNIT_DETAILS_LIST[i].legal_entity_name){
                    legal_entity_id = value.legal_entity_id;
                }
            });
        }
    }
    return {
        "unit_id": parseInt(unit_id),
        "domain_name": domain_name,
        "legal_entity_id": legal_entity_id
    }
}

// Save the assigned units
$(".save-assign-unit").click(function(){
    domain_manager_id = $("#userid").val().trim();
    mgr_name = $('#assinee').val().trim();
    var true_count = ASSIGN_UNIT_SAVE_DETAILS.length;
    var active_units = []
    /*$.each(ASSIGN_UNIT_SAVE_DETAILS, function(unit_id, unit_value){
        $.each(unit_value, function(domain_name, value){
            if(value == true || value == "true"){
                ++true_count;
                active_units.push(
                    getActiveUnitDict(unit_id, domain_name)
                );
            }
        });
    });*/
    if(true_count > 0 && (domain_manager_id != null && domain_manager_id != '') && (mgr_name != null && mgr_name != '')){
        for(var i=0;i<ASSIGN_UNIT_SAVE_DETAILS.length;i++){
            //DOMAIN_NAME
            active_units.push(
                getActiveUnitDict(ASSIGN_UNIT_SAVE_DETAILS[i], DOMAIN_NAME)
            );
        }
        callSaveAssignUnitAPI(parseInt(domain_manager_id), active_units);
    }
    else{
        if(true_count <= 0){
            displayMessage(message.atleast_one_unit_required);
        }
        else if((domain_manager_id == null || domain_manager_id == '') || (mgr_name == null || mgr_name == '')){
            if(USER_CAREGORY == "Domain Manager"){
                displayMessage(message.domain_manager_required);
            }else{
                displayMessage(message.domain_executive_required);
            }
            //USER_CAREGORY
        }
    }
});

// Invokes the api for saving the assigned units
function callSaveAssignUnitAPI(domain_manager_id, unit_ids){
    function onSuccess(data) {
        displaySuccessMessage(message.assign_success);
        initialize("list");
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.saveAssignedUnits(CLIENT_ID, domain_manager_id, unit_ids,
        function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                hideLoader();
                onFailure(error);
            }
        }
    );
}


// Form Initialization
$(function(){
	initialize("list");
});

// JS-Filterable for filtering the records
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});
$(document).find('.js-filtertable-domain').each(function(){
    $(this).filtertable().addFilter('.js-filter-domain');
});
$(document).find('.js-filtertable-view').each(function(){
    $(this).filtertable().addFilter('.js-filter-view');
});

