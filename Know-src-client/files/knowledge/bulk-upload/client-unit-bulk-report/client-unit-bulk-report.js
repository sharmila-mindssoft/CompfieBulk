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
var Show_btn = $('#show');
var Export_btn = $('#export');
var fromDate = $("#from-date");
var toDate = $("#to-date");



s_page = null;


var UserCategoryID=0;
var TechnoExecutives=[];


// get client unit bulk upload report data from api
function processSubmit() {
    
    // var Country = data.user_details.country_ids;
    // var Domain = data.user_details.domain_ids;


    var FromDate = fromDate.val();
    var ToDate = toDate.val();
    var ClientGroup = GroupId.val();
        
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
            "child_ids" : TechnoExecutives,
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

    Show_btn.click(function() {
        is_valid = s_page.validateMandatory();
        if (is_valid == true) {
            s_page._on_current_page = 1;
            s_page._total_record = 0;
       /*     s_page.fetchData();
            s_page.renderPageControls();*/

        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
            });

        on_current_page = 1;
        /*$('.country').text("Country: " + Country.val());
        $('.domain').text("Domain: " + Domain.val());*/
         processSubmit();
         }
    });

}



function fetchFiltersData() {
    displayLoader();

    //alert('display');
    mirror.getClientLoginTraceFilter(
        function(error, response) {
            console.log(response)
            if (error != null) {
                hideLoader();
                displayMessage(error);
            } else {
                _clientUsers = response.audit_client_users;
                _clients = response.clients;
                loadCurrentUserDetails();
                hideLoader();
            }
        }
    );
}


function loadCurrentUserDetails()
{
    //alert('load Current User Details');
    var user = mirror.getUserInfo();
    var logged_user_id=0;
    
     $.each(allUserInfo, function(key, value){
        if(user.user_id==value["user_id"]) {
            UserCategoryID=value["user_category_id"];
            logged_user_id=value["user_id"];
            console.log(UserCategoryID);
        }
     });

    //alert('TE'+user.employee_code);

    if(UserCategoryID==6)
    {   
     //alert('TE'+user.employee_code);
        // TE-Name  : Techno-Executive 
        $('.active-techno-executive').attr('style','display:block');
        $('#techno-name').text(user.employee_code+" - "+user.employee_name.toUpperCase());
    }
    else if(UserCategoryID==5 && UserCategoryID!=6 && logged_user_id>0)
    {
        // TE-Name  : Techno-Manager 
        getUserMappingsList(logged_user_id);
    }
    
}

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    console.log(id_element)
    var current_id = id_element[0].id;
    // if (current_id == "group-id") {
    //     clearElement([users, userId]);
    // }
}




//get client unit bulk report filter details from api
function getClientUnits() {
    function onSuccess(data) {

        // countriesList = data.countries;
        // domainsList = data.domains;
        allUserInfo = data.user_details;
        // userDetails = data.user_details[0];
        // Domain_ids = userDetails.country_wise_domain;
        // EmpCode = userDetails.employee_code;
        // EmpName = userDetails.employee_name;        


        //Load Countries MultiSelectBox
        // for (var countiesOpt in countriesList) {
        //     var option = $('<option></option>');
        //     option.val(countriesList[countiesOpt].country_id);
        //     option.text(countriesList[countiesOpt].country_name);
        //     $('#country').append(option);
        // }
        // $('#country').multiselect('rebuild');
        loadCurrentUserDetails();
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getAdminUserList(function(error, response) {
        if (error == null)
        {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
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


function Client_unit_bulk_report_page() {
    // this._sno = 0;
    // this._userList = {};
    // this._formList = {};
    // this._categoryList = {};
    // this._auditData = {};
    // this._auditFormData = {};
    // this._clientUsers = {};
    // this._clientForms = {};
    // this._clients = {};
    // this._businessGroups = {};
    // this._legalEntities = {};
    // this._divisions = {};
    // this._divCategories = {};
    // this._unitList = {};
    // this._on_current_page = 1;
    // this._sno = 0;
    // this._total_record = 0;
    // this._csv = false;
}


// Fields Manadory validation 
Client_unit_bulk_report_page.prototype.validateMandatory = function()
{
    is_valid = true;

    if (GroupId.val().trim() == '' || GroupId.val().trim() == null) {
        displayMessage(message.group_required);
        is_valid = false;
    } 
    else if (this.getValue("from-date") == "")
    {
        displayMessage(message.fromdate_required);
        is_valid = false;
    }
    else if (this.getValue("to-date") == "")
    {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};


// To get the corresponding value
Client_unit_bulk_report_page.prototype.getValue = function(field_name, f_id)
{
    if (field_name == "from-date")
    {
        f_date = fromDate.val().trim();
        return f_date;
    }
    else if (field_name == "to-date")
    {
        f_date = toDate.val().trim();
        return f_date;
    } 
};




//display client unit bulk upload details according to count
function loadCountwiseResult(filterList) {
    $('.tbody-compliance').empty();
    lastActName = '';
    lastOccuranceid = 0;
    var showFrom = sno + 1;
    var is_null = true;
    for (var entity in filterList) {

        is_null = false;
        sno = parseInt(sno) + 1;
        //var country_name = filterList[entity].country_name;
        //var domain_name = filterList[entity].domain_name;
        var csv_name = filterList[entity].csv_name;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var uploaded_by = filterList[entity].uploaded_by;
        var uploaded_on = filterList[entity].uploaded_on;
        var total_rejected_records = filterList[entity].total_rejected_records;
        var rejected_on = filterList[entity].rejected_on;
        var rejected_by = filterList[entity].rejected_by;
        var reason_for_rejection = filterList[entity].is_fully_rejected;
        var approve_status = filterList[entity].approve_status;
        

       
        if(parseInt(uploaded_by)==userDetails.user_id){
            EmpCode = userDetails.employee_code;
            EmpName = userDetails.employee_name;
            uploaded_by=EmpCode+" - "+ EmpName.toUpperCase();
        }
        if(parseInt(reason_for_rejection)==1){
            reason_for_rejection="Fully Rejected";
        }
        else{
            reason_for_rejection="- -";   
        }
        
        var occurance = '';
        var occuranceid;

        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();

        $('.tbl_sno', clone1).text(sno);        
        //$('.tbl_country', clone1).text(country_name);
        //$('.tbl_domain', clone1).text(domain_name);
        $('.tbl_uploaded_file_name', clone1).text(csv_name);
        $(".tbl_uploaded_by", clone1).text(uploaded_by);
        $('.tbl_uploaded_on', clone1).text(uploaded_on);
        $('.tbl_no_of_tasks', clone1).text(tbl_no_of_tasks);
        $('.tbl_approved_rejected_tasks', clone1).text(approve_status+" / "+total_rejected_records);
        $('.tbl_approved_rejected_on', clone1).text(rejected_on);
        $('.tbl_approved_rejected_by', clone1).text(rejected_by);
        $('.tbl_reason_for_rejection', clone1).text(reason_for_rejection);
        $('#datatable-responsive .tbody-compliance').append(clone1);
        
        compliance_count = compliance_count + 1;
        lastActName = country_name;
    }

    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}













// Instance Creation of the page class
s_page = new Client_unit_bulk_report_page();

// Form Initalize
$(function() {
    //resetFields();
    //loadItemsPerPage();
    getClientUnits();
    PageControls();
    fetchFiltersData();
});



