/******************* 

API         -  getAdminUserList 
Input Field -  Client Group
var UserGroup; // UserGroup = data.user_groups;



**************/

/***********    
API         - getUserMappings
Input Field - TE Name

var UserMappings; // getUserMappings=data.user_mappings
var logged_user_id; // Session UserID

Check the If Conditions to get the Associative TechnoExecutives list of TechnoManagers(CurrentUser)
if(logged_user_id==value.parent_user_id)

Get the TechnoExecutiveName and UserID by using below API

API - getAdminUserList
var allUserInfo = data.user_details
--value.user_id
--value.employee_name
--value.employee_code
--value.user_category_id 
--value.country_ids         // Generate Countries Array
--value.country_wise_domain //  Generate Domain Array
************/


/***************    Client Unit - Bulk Upload Report


***************/



// get Client Unit - Bulk Upload Report

var GroupName = $("#groupsval");
var GroupId = $("#group-id");
var ACGroup = $("#ac-group");

var UserCategoryID=0;

function processSubmit() {
    
    var Country = data.user_details.country_ids;
    var Domain = data.user_details.domain_ids;


    var FromDate = $('#from-date').val();
    var ToDate = $('#to-date').val();
    var ClientGroup = $('#ClientGroup').val();
    var TEName = $('#TEName').val();
        
    var SelectedCountryId=[];
    var SelectedTechnoIds=[];
    var SplitValues;

        /* multiple COUNTRY selection in to generate array */
        $.each(Country, function(key, value){
            SelectedCountryId.push(parseInt(value));
        });

        /* multiple DOMAIN selection generate as a array */
        $.each(TEName, function(key, value){
            SelectedTechnoIds.push(parseInt(value));
        });

        displayLoader();
        _page_limit = parseInt(ItemsPerPage.val());

        if (on_current_page == 1) {
            sno = 0
        } else {
            sno = (on_current_page - 1) * _page_limit;
        }

        filterdata = {
            "c_ids": SelectedCountryId,
            "d_ids": SelectedDomainId,
            "from_date": FromDate,
            "to_date" : ToDate,
            "r_count" : sno,
            "p_count" : _page_limit,
            "child_ids" : SelectedTechnoIds,
            "user_category_id" : UserCategoryID
        };

        bu.getStatutoryMappingsBulkReportData(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
}

function PageControls() {
    GroupName.keyup(function(e) {
        //alert('client group autocomplete');

        var textval = $(this).val();
        commonAutoComplete(
            e, ACGroup, GroupId, textval,
            _clients, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupName, GroupId, val);
            });

    });

}


//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    console.log(id_element)
    var current_id = id_element[0].id;
    if (current_id == "group-id") {
        clearElement([users, userId]);
    }
}

function fetchFiltersData() {
    displayLoader();

    //alert('displauy');
    mirror.getClientLoginTraceFilter(
        function(error, response) {
            console.log(response)
            if (error != null) {
                hideLoader();
                displayMessage(error);
            } else {
                _clientUsers = response.audit_client_users;
                _clients = response.clients;
                hideLoader();
            }
        }
    );
}

function loadCurrentUserDetails()
{
    var user = mirror.getUserInfo();
    var logged_user_id=0;
    
     $.each(allUserInfo, function(key, value){
        if(user.user_id==value["user_id"]) {
            UserCategoryID=value["user_category_id"];
            logged_user_id=value["user_id"];
            console.log(UserCategoryID);
        }
     });

    if(UserCategoryID==6)
    {   
        // KE-Name  : Knowledge-Executive 
        $('.active-techno-executive').attr('style','display:block');
        $('#techno-name').text(user.employee_code+" - "+user.employee_name.toUpperCase());
    }
    else if(UserCategoryID==5 && UserCategoryID!=6 && logged_user_id>0)
    {
        // KE-Name  : Knowledge-Manager 
        getUserMappingsList(logged_user_id);
    }
    
}


//get client unit bulk upload report filter details from api
function getUserMappingsList(logged_user_id) {
    $('.form-group-tename-tmanager').attr("style","display:block !important");
    $('#tename-tmanager').multiselect('rebuild');
    function onSuccess(logged_user_id, data){

        var userMappingData=data;
        var d;
        $.each(userMappingData.user_mappings, function(key, value)
        {
            if(logged_user_id==value.parent_user_id)
            {
                TechnoExecutives.push(value.child_user_id);
                childUsersDetails(allUserInfo, logged_user_id, value.child_user_id)
            }
        });
    }
    function childUsersDetails(allUserInfo, parent_user_id, child_user_id)
    {
        $.each(allUserInfo, function(key, value)
        {
         if(child_user_id==value["user_id"] && value["is_active"]==true) {
            
            var option = $('<option></option>');
            option.val(value["user_id"]);
            option.text(value["employee_code"]+" - "+value["employee_name"]);
            $('#tename-tmanager').append(option);
         }
        });
        $('#tename-tmanager').multiselect('rebuild');
    }

    function onFailure(error){
        displayMessage(error);
        hideLoader();
    }

    mirror.getUserMappings(function(error, response) {
        if (error == null)
        {
            onSuccess(logged_user_id, response);    
        } else {
            onFailure(error); 
        }
    });

}

// Form Initalize
$(function() {
    //resetFields();
    //loadItemsPerPage();
    PageControls();
    fetchFiltersData();
});



