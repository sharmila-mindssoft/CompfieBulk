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