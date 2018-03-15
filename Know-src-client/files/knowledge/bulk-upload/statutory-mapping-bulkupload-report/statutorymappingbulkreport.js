var statutoryMappingReportDataList;
var complianceFrequencyList;

var SystemRejected="COMPFIE";

var count = 1;
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord = 0;
var ReportView = $('.grid-table-rpt');

var compliance_count = 0;

var ItemsPerPage = $('#items_per_page');
var Show_btn = $('#show');
var Export_btn = $('#export');


var Country = $('#country');
var Domain = $('#domain');
var ToDate = $("#to-date");
var FromDate = $("#from-date");


var Country_ids = [];
var Domain_ids = [];
var EmpCode;
var EmpName;
s_page = null;

var UserCategoryID = 0;
var KnowledgeExecutives = [];
var ALLUSERS = [];
var CSV = false;


function Statutory_mapping_bulk_report_page() {
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

// To get the corresponding value
Statutory_mapping_bulk_report_page.prototype.getValue = function(field_name, f_id)
{
    if (field_name == "from-date")
    {
        f_date = FromDate.val().trim();
        return f_date;
    }
    else if (field_name == "to-date")
    {
        f_date = ToDate.val().trim();
        return f_date;
    }
};

// Fields Manadory validation
Statutory_mapping_bulk_report_page.prototype.validateMandatory = function()
{
    is_valid = true;

    if ($('#country option:selected').text() == "")
    {
        displayMessage(message.country_required);
        is_valid = false;
    }
    else if ($('#domain option:selected').text() == "")
    {
        displayMessage(message.domain_required);
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

//get statutory mapping bulk report filter details from api
function getStatutoryMappings() {
    function onSuccess(data) {

        countriesList = data.countries;
        domainsList = data.domains;
        allUserInfo = data.user_details;
        userDetails = data.user_details[0];
        Domain_ids = userDetails.country_wise_domain;
        EmpCode = userDetails.employee_code;
        EmpName = userDetails.employee_name;


        //Load Countries MultiSelectBox
        for (var countiesOpt in countriesList) {
            var option = $('<option></option>');
            option.val(countriesList[countiesOpt].country_id);
            option.text(countriesList[countiesOpt].country_name);
            $('#country').append(option);
        }
        $('#country').multiselect('rebuild');
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

//display statutory mapping details according to count
function loadCountwiseResult(filterList) {
    $('.tbody-compliance').empty();
    lastActName = '';
    lastOccuranceid = 0;
    var showFrom = sno + 1;
    var is_null = true;
    for (var entity in filterList) {

        is_null = false;
        sno = parseInt(sno) + 1;
        var country_name = filterList[entity].country_name;
        var domain_name = filterList[entity].domain_name;
        var csv_name = filterList[entity].csv_name_text;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var uploaded_by = filterList[entity].uploaded_by;
        var uploaded_on = filterList[entity].uploaded_on;
        var total_rejected_records = filterList[entity].total_rejected_records;
        var rejected_on = filterList[entity].rejected_on;
        var rejected_by = filterList[entity].rejected_by;
        var reason_for_rejection = filterList[entity].is_fully_rejected;
        var approve_status = filterList[entity].approve_status;

        /*  if(parseInt(uploaded_by)==userDetails.user_id){
            EmpCode = userDetails.employee_code;
            EmpName = userDetails.employee_name;
            uploaded_by=EmpCode+" - "+ EmpName.toUpperCase();
        }*/
        $(allUserInfo).each(function(key,value)
        {
            if(parseInt(uploaded_by) == value["user_id"])
            {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                uploaded_by = EmpCode + " - " + EmpName.toUpperCase();
            }
            else if(parseInt(rejected_by) == value["user_id"])
            {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                rejected_by = EmpCode + " - " + EmpName.toUpperCase();
            }
        });
        if(parseInt(reason_for_rejection) == 1){
            reason_for_rejection = "Fully Rejected";
        }
        else{
            reason_for_rejection = "- -";
        }

        var occurance = '';
        var occuranceid;

        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();

        $('.tbl_sno', clone1).text(sno);
        $('.tbl_country', clone1).text(country_name);
        $('.tbl_domain', clone1).text(domain_name);
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

// get statutory mapping report data from api
function processSubmit() {
    var country = $('#country').val();
    var domain = $('#domain').val();
    var from_date = $('#from-date').val();
    var to_date = $('#to-date').val();
    var keNamesSelected = [];

    var selectedCountryId = [];
    var selectedDomainId = [];
    var splitValues;

        /* multiple COUNTRY selection in to generate array */
        $.each(country, function(key, value){
            selectedCountryId.push(parseInt(value));
        });

        /* multiple DOMAIN selection generate as a array */
        $.each(domain, function(key, value){
            splitValues = value.split("-");
            selectedDomainId.push(parseInt(splitValues[1]));
        });

        if($('#kename-kmanager').val() == null){
            keNamesSelected = KnowledgeExecutives;
        }else{
            $('#kename-kmanager > option:selected').each(function() {
                console.log(this.value);
                keNamesSelected.push(parseInt(this.value));
            });
        }

        console.log("Kenames selected-> " + keNamesSelected);
        displayLoader();
        _page_limit = parseInt(ItemsPerPage.val());

        if (on_current_page == 1) {
            sno = 0
        } else {
            sno = (on_current_page - 1) * _page_limit;
        }

        filterdata = {
            "c_ids": selectedCountryId,
            "d_ids": selectedDomainId,
            "from_date": from_date,
            "to_date" : to_date,
            "r_count" : sno,
            "p_count" : _page_limit,
            "child_ids" : keNamesSelected,
            "user_category_id" : UserCategoryID
        };
        function onSuccess(data) {
            $('.details').show();

            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
                $(this).show();
            });


            sno = sno;

            statutoryMappingReportDataList = data.reportdata;

            /*totalRecord = data.total_count*/;
            totalRecord = data.total;

            hideLoader();

            if (totalRecord == 0) {
                $('.tbody-compliance').empty();
                var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
                var clone4 = tableRow4.clone();
                $('.tbl_norecords', clone4).text('No Records Found');
                $('.tbody-compliance').append(clone4);
                PaginationView.hide();
                ReportView.show();
                hideLoader();
            } else {
                hideLoader();
                if (sno == 0) {
                    createPageView(totalRecord);
                }
                PaginationView.show();
                ReportView.show();
                loadCountwiseResult(statutoryMappingReportDataList);
            }

        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }
        bu.getStatutoryMappingsBulkReportData(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
        //temp_act = act;
    //}
}

function loadDomains() {

    /******** Load Domain Lists *********/
    Domain.empty();
    if (Country.val() != null)
    {
        var sCountries = Country.val().map(Number);
        var str = '';

        $.each(countriesList, function(key, value)
        {
            var cId = value.country_id;

            if ($.inArray(cId, sCountries) >= 0)
            {
                var flag = true;

                $.each(domainsList, function(key1, v)
                {

                    if (v.is_active == false)
                    {
                        return;
                    }

                    if ($.inArray(cId, v.country_ids) >= 0)
                    {
                        var sText = '';
                        $.each(Domain_ids, function(key2, value2)
                        {
                            if (v.domain_id == value2.d_id && cId == value2.c_id)
                            {
                                sText = 'selected="selected"'
                            }
                        });

                        if (flag)
                        {
                            str += '<optgroup label="' + value.country_name + '">';
                        }

                        var dVal = cId + '-' + v.domain_id;
                        str += '<option value="' + dVal + '" ' + sText + '>' + v.domain_name + '</option>';
                        flag = false;
                    }
                });
                if (flag == false) str += '</optgroup>'
            }
        });
        $('#domain').append(str);
        $('#domain').multiselect('rebuild');
  }

}

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

function hidePagePan() {
    CompliacneCount.text('');
    PaginationView.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    Pagination.empty();
    Pagination.removeData('twbs-pagination');
    Pagination.unbind('page');

    Pagination.twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                processSubmit();
            }
        }
    });
};
function pageControls() {

   /**** Load Domain List When MultiSelecting The Countries **********/
   Country.change(function(){
        $('#domain').empty();
        $('#domain').html();
        //$('#domain').append('None Selected');
        $('#domain').multiselect('rebuild');
        loadDomains();
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        sno = 0;
        on_current_page = 1;
        createPageView(totalRecord);
        processSubmit();
    });

    Show_btn.click(function() {
        is_valid = s_page.validateMandatory();
        if (is_valid == true) {
            s_page._on_current_page = 1;
            s_page._total_record = 0;
        $('#mapping_animation').
        removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd '+
            'mozAnimationEnd MSAnimationEnd oanimationend animationend',
            function(){
                $(this).removeClass();
            });
             on_current_page = 1;
             processSubmit();
         }
    });


    Export_btn.click(function(e) {
        is_valid = s_page.validateMandatory();
        if (is_valid == true) {
            CSV = true;
            s_page.exportData();
        }
    });
}

function loadCurrentUserDetails(){
    var user = mirror.getUserInfo();
    var logged_user_id = 0;
    var knowledgeName;
    var kUserdetails = {};

     $.each(allUserInfo, function(key, value){
        if(user.user_id == value["user_id"]) {
            UserCategoryID = value["user_category_id"];
            logged_user_id = value["user_id"];
        }
     });

    if(UserCategoryID == 4){
        // KE-Name  : Knowledge-Executive
        knowledgeName = user.employee_code + " - "
                        + user.employee_name.toUpperCase()
        $('.active-knowledge-executive').attr('style','display:block');
        $('#knowledge-name').text(knowledgeName);

        kUserdetails={
            /*"user_name":knowledgeName,*/
            "user_id":user.user_id
        }

        ALLUSERS.push(kUserdetails);
        KnowledgeExecutives.push(user.user_id);

    }
    else if(UserCategoryID == 3 && UserCategoryID != 4 && logged_user_id > 0){
        // KE-Name  : Knowledge-Manager
        getUserMappingsList(logged_user_id);
    }
    console.log("ALLUSERS >>>>>>>>>>");
    console.log(ALLUSERS);

}

//get statutory mapping bulk report filter details from api
function getUserMappingsList(logged_user_id) {
    $('.form-group-kename-kmanager').attr("style","display:block !important");
    $('#kename-kmanager').multiselect('rebuild');
    function onSuccess(logged_user_id, data){
        console.log("logged_user_id->"+ logged_user_id);
        var userMappingData = data;
        var d;
        $.each(userMappingData.user_mappings, function(key, value){
            if(logged_user_id == value.parent_user_id){
                console.log("value.child_user_id-> "+ value.child_user_id);
                console.log("inaary-> "+jQuery.inArray(value.child_user_id, KnowledgeExecutives));
                if(jQuery.inArray(value.child_user_id, KnowledgeExecutives) == -1){
                    console.log("inif")
                    KnowledgeExecutives.push(value.child_user_id);
                    childUsersDetails(allUserInfo, logged_user_id, value.child_user_id)
                }
            }
        });
    }
    function childUsersDetails(allUserInfo, parent_user_id, child_user_id){
        var kUserdetails={}
        $.each(allUserInfo, function(key, value){
            if(child_user_id == value["user_id"] && value["is_active"]==true) {

            var option = $('<option></option>');
            option.val(value["user_id"]);
            option.text(value["employee_code"]+" - "+value["employee_name"]);
            $('#kename-kmanager').append(option);

            knowledgeName = value["employee_code"] +" - "+ value["employee_name"].toUpperCase()
            kUserdetails={
                "name":knowledgeName,
                "user_id":value["user_id"]
            }

            ALLUSERS.push(kUserdetails);

         }
        });


        $('#kename-kmanager').multiselect('rebuild');
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


// Instance Creation of the page class
s_page = new Statutory_mapping_bulk_report_page();

//initialization
$(function() {
    displayLoader();
    $('.grid-table-rpt').hide();
    pageControls();
    loadItemsPerPage();
    getStatutoryMappings();
    $('#country').focus();
});

$(document).ready(function(){
    $(document).on("contextmenu",function(e){
        e.preventDefault();
    });

 });


//To export data
Statutory_mapping_bulk_report_page.prototype.exportData = function() {

    var country = $('#country').val();
    var domain = $('#domain').val();
    var fromDate = $('#from-date').val();
    var toDate = $('#to-date').val();
    var selectedCountryId = [];
    var selectedDomainId = [];
    var splitValues;
    var downloadCSV = true;
    var keNamesSelected = [];
    // multiple COUNTRY selection in to generate array
    $.each(country, function(key, value){
        selectedCountryId.push(parseInt(value));
    });

    var countryNames = $("#country option:selected").map(function () {
        return $(this).text();
    }).get().join(',');

    console.log("countryNames-> "+ countryNames);

    // multiple DOMAIN selection generate as a array
    $.each(domain, function(key, value){

        splitValues=value.split("-");
        selectedDomainId.push(parseInt(splitValues[1]));
    });

    var domainNames = $("#domain option:selected").map(function () {
        return $(this).text();
    }).get().join(',');

    console.log("domainNames-> "+ domainNames);

   if($('#kename-kmanager').val() == null){
            keNamesSelected = KnowledgeExecutives;
    }else{
            $('#kename-kmanager > option:selected').each(function() {
                console.log(this.value);
                keNamesSelected.push(parseInt(this.value));
            });
    }

    console.log("Kenames selected-> " + keNamesSelected);

    filterdata = {
            "c_ids": selectedCountryId,
            "c_names": countryNames,
            "d_ids": selectedDomainId,
            "d_names": domainNames,
            "child_ids" : keNamesSelected,
            "from_date": fromDate,
            "to_date": toDate,
            "csv": downloadCSV,
            "user_category_id": UserCategoryID
            /*"dependent_users":ALLUSERS*/
        };

    displayLoader();
    bu.exportSMBulkReportData(filterdata,
        function(error, response) {
            if (error == null) {
                hideLoader();
                if (CSV) {
                    var download_url = response.link;
                    $(location).attr('href', download_url);
                }
            }
            else {
                hideLoader();
                if (error == "ExportToCSVEmpty") {
                    displayMessage(message.empty_export);
                }else {
                    displayMessage(error);
                }
            }
        });

};

