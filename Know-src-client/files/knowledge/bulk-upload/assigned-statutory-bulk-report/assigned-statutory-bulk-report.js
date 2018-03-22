//variable declaration
var TOTALRECORD;
var ALLUSERINFO;
var USERDETAILS;
var CLIENTLIST;
var ASSIGNEDUNITLIST;
var MAPPEDUSERLIST;
var USERMAPPINGLIST;
var CSV = false;

var USERACCESSCOUNTRIESIDS=[];
var DOMAINEXECUTIVES=[];
var USERCATEGORYID;

var EXISTINGUSERID=[];

//Input field variable declaration

var TODATE=$("#to_date");
var FROMDATE=$("#from_date");

var SHOW_BTN = $('#show');
var EXPORT_BTN = $('#export');


//Pagination variable declaration
var ITEMSPERPAGE = $('#items_per_page');
var PAGINATIONVIEW = $('.pagination-view');
var PAGINATION = $('#pagination-rpt');
var COMPLIACNECOUNT = $('.compliance_count');
var COMPLIANCE_COUNT = 0;

var DENAME=$('#dename-dmanager');
var ON_CURRENT_PAGE = 1;
var SNO = 0;

var _page_limit = 25;


var ReportView = $('.grid-table-rpt');
var ACGroup = $('#ac-group');
var ACLegalEntity = $('#ac-legalentity');
var ACUnit = $('#ac-unit');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');
var UnitVal = $('#unitval');
var Unit = $('#unitid');
var Domain = $('#domain');



s_page = new AssignStatutoryBulkReport();

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
//load all the filters
function initialize() {
  function onSuccess(data) {
    DomainList = data.domains;
    allUserInfoList();
    resetAllfilter();
    resetFields();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getAdminUserList(function (error, response) {
    if (error == null) {
      onSuccess(response);
      hideLoader();
    } else {
      onFailure(error);
      hideLoader();
    }
  });
}

//load all the filters
function UserGroupDetails() {
  function onSuccess(data) {
    CLIENTLIST = data.usermapping_groupdetails;
    legelEntityList = data.usermapping_legal_entities;
    ASSIGNEDUNITLIST = data.statutory_unit;

    resetAllfilter();
    resetFields();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getUserMappingStatutoryFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
      hideLoader();
    } else {
      onFailure(error);
      hideLoader();
    }
  });
}
function resetAllfilter() {
  GroupVal.val('');
  LegalEntityVal.val('');
  UnitVal.val('');

  $('.tbody-usermappingdetails-list').empty();
  $('.grid-table-rpt').hide();
  $('.details').hide();
}
function resetfilter(evt)
{

  if(evt=='clients')
  {
    LegalEntityVal.val('');
    LegalEntity.val('');

    Domain.empty();
    Domain.html();
    Domain.multiselect('rebuild');

    UnitVal.val('');
    Unit.val('');

    FROMDATE.val('');
    TODATE.val('');

    DENAME.multiselect("deselectAll", false);
    DENAME.multiselect('refresh');

  }
  if(evt == 'le')
  {
    Domain.empty();
    Domain.html();
    Domain.multiselect('rebuild');

    UnitVal.val('');
    UnitVal.val('');

    FROMDATE.val('');
    TODATE.val('');

    DENAME.multiselect("deselectAll", false);
    DENAME.multiselect('refresh');

  }
  if(evt == 'domains')
  {
    UnitVal.val('');
    UnitVal.val('');

    FROMDATE.val('');
    TODATE.val('');

  }

  $('.tbody-usermappingdetails-list').empty();
  $('.grid-table-rpt').hide();
  $('.details').hide();
}


//pagination - functions
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    COMPLIACNECOUNT.text(showText);
    PAGINATIONVIEW.show();
}

function hidePagePan() {
    COMPLIACNECOUNT.text('');
    PAGINATIONVIEW.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ITEMSPERPAGE.val());
    PAGINATION.empty();
    PAGINATION.removeData('twbs-pagination');
    PAGINATION.unbind('page');

    PAGINATION.twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(ON_CURRENT_PAGE) != cPage) {
                ON_CURRENT_PAGE = cPage;
                $('#show-button').trigger( "click" );
                processSubmit();
            }
        }
    });
};

function processPaging(){
  _page_limit = parseInt(ITEMSPERPAGE.val());
  showFrom = SNO + 1;
  if (ON_CURRENT_PAGE == 1) {
    SNO = 0
  }
  else {
    SNO = (ON_CURRENT_PAGE - 1) *  _page_limit;
  }
  SNO  = SNO;
  if (TOTALRECORD == 0) {
    /*loadHeader();*/
    hideLoader();
    $('.tbody-usermappingdetails-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-usermappingdetails-list').append(clone4);
    //ExportButton.hide();
    PAGINATIONVIEW.hide();

  } else {
    if(SNO==0){
      //ExportButton.show();
      createPageView(TOTALRECORD);
    }
    PAGINATIONVIEW.show();
    //ReportView.show();

    loadUserMappingDetailsList();
  }
}

function pageData(ON_CURRENT_PAGE){
  data = [];
  _page_limit = parseInt(ITEMSPERPAGE.val());
  recordLength = (parseInt(ON_CURRENT_PAGE) * _page_limit);
  var showFrom = SNO + 1;
  var is_null = true;
  for(i=SNO;i<MAPPEDUSERLIST.length;i++)
  {
    is_null = false;
    data.push(MAPPEDUSERLIST[i]);
    if(i == (recordLength-1))
    {
      break;
    }
  }
  if (is_null == true) {
    hidePagePan();
  }
  else {
    if(recordLength < TOTALRECORD)
      showPagePan(showFrom, recordLength, TOTALRECORD);
    else
      showPagePan(showFrom, TOTALRECORD, TOTALRECORD);
  }
  return data;
}
function resetFields(){
  Group.val('');
  $('#legalentityid').val('');
  $('#unitid').val('');
}

function loadUserMappingDetailsList()
{
  var th_cnt=3;

  var is_null = true;
  $('.tbody-usermappingdetails-list').empty();
  $('.usermapping-header').empty();
  //$('.#datatable-responsive').empty();
  domainsList = USERMAPPINGLIST.usermapping_domain;
  /*loadHeader();*/

  //$('#datatable-responsive th').remove();

  var tableheading = $('#templates .tr-heading');
  var cloneheading = tableheading.clone();
  $('.usermapping-header').append(cloneheading);

  if(domainsList.length > 0)
  {
    for(var i=0;i<domainsList.length;i++)
    {
      is_null = false;
      $('.usermapping-header th:last-child').each(function() {
        for(var j=1;j<=2;j++)
        {
          var clone = $(this).clone().html('&nbsp;');
          if (clone.is('th')) {
            if(j==1)
            {
              clone.text('Domain Manager '+domainsList[i].domain_name);
            }
            else
            {
              clone.text('Domain User '+domainsList[i].domain_name);
            }
          }
          $(this).parent().append(clone);
          th_cnt = th_cnt + 1;
        }
      });
    }
  }
  //load details
  technoDetails = USERMAPPINGLIST.techno_details;
  var assignedDomainVal = '';
  var assignedDomainVal_1 = '';
  var getDomainVal  = '';
  var col=4;
  for(var i=0;i<technoDetails.length;i++)
  {
    is_null = false;
    //alert(technoDetails.length);
    assignedDomainVal = '';
    var tableRow = $('#templates .table-row');
    var clone1 = tableRow.clone();
    SNO = SNO + 1;
    $('.SNO', clone1).text(SNO);
    //var unit_code_name = getUnitName(technoDetails[i].unit_id);
    $('.unit-name', clone1).text(technoDetails[i].unit_code_with_name);
    $('.techno-manager', clone1).text(technoDetails[i].techno_manager);
    $('.techno-user', clone1).text(technoDetails[i].techno_user);
    $('.tbody-usermappingdetails-list').append(clone1);
    for(var k=col;k<=th_cnt;k++)
    {
      var headerObj = $('#datatable-responsive').find('th').eq(k);
      getDomainVal = getDomainAssigned(headerObj.text(), technoDetails[i].unit_id, USERMAPPINGLIST);
      if(assignedDomainVal == '')
      {
        assignedDomainVal  = getDomainVal;
      }
      else
      {
        assignedDomainVal  = assignedDomainVal +"," + getDomainVal;
      }
    }
    if(assignedDomainVal_1 == '')
    {
      assignedDomainVal_1  = assignedDomainVal;
    }
    else
    {
      assignedDomainVal_1  = assignedDomainVal_1 +";"+assignedDomainVal;
    }
  }
  var split_domain_with_colon = "";
  if(assignedDomainVal_1.indexOf(";") > 0)
    split_domain_with_colon = assignedDomainVal_1.split(";");
  else
    split_domain_with_colon = assignedDomainVal_1;
  var row_indx = 0;
  $('.tbody-usermappingdetails-list tr :last-child').each(function() {
    var index = $(this).closest('td').index();
    if(index > 0 && assignedDomainVal_1.indexOf(";") < 0)
    {
      var split_domain_with_comma = split_domain_with_colon.split(",");
      for(var k=0;k<split_domain_with_comma.length;k++)
      {
        var clone2 = $(this).clone().html('&nbsp;');
        if (clone2.is('td')) {
          clone2.text(split_domain_with_comma[k]);
        }
        $(this).parent().append(clone2);
      }
    }
    else
    {
      if(index > 0)
      {
        for(var m=row_indx;m<split_domain_with_colon.length;m++){
          var split_domain_with_comma = split_domain_with_colon[m].split(",");
          for(var k=0;k<split_domain_with_comma.length;k++)
          {
            var clone2 = $(this).clone().html('&nbsp;');
            if (clone2.is('td')) {
              clone2.text(split_domain_with_comma[k]);
            }
            $(this).parent().append(clone2);
          }
          row_indx = row_indx + 1;
          break;
        }
      }
    }
  });
  if(is_null == false)
    showPagePan(showFrom, SNO, TOTALRECORD);
}


//get statutory mapping bulk report filter details from api
function allUserInfoList() {
    function onSuccess(data) {
        ALLUSERINFO = data.user_details;
        loadCurrentUserDetails();
    }
    function onFailure(error) {
        displayMessage(error);
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

// Check If Current User Is Domain Manager Or Executives
function loadCurrentUserDetails()
{
    var user = mirror.getUserInfo();
    var logged_user_id=0;

        if(ALLUSERINFO){
         $.each(ALLUSERINFO, function(key, value){
            if(user.user_id==value["user_id"]) {
                UserCategoryID=value["user_category_id"];
                logged_user_id=value["user_id"];

            }
         });

        if(UserCategoryID==8)
        {
            // De-Name  : Domain-Executive
            $('.active-domain-executive').attr('style','display:block');
            $('.form-group-dename-dmanager').attr("style","display:none !important");
            $('#domain-name').text(user.employee_code+" - "+user.employee_name.toUpperCase());
            EXISTINGUSERID.push(logged_user_id);
        }
        else if(UserCategoryID==7 && UserCategoryID!=8 && logged_user_id>0)
        {
            // DE-Name  : Domain-Manager
            getUserMappingsList(logged_user_id);
        }
    }

}

//get statutory mapping bulk report filter details from api
function getUserMappingsList(logged_user_id) {

    $('.form-group-dename-dmanager').attr("style","display:block !important");
    $('#dename-dmanager').multiselect('rebuild');
    function onSuccess(logged_user_id, data){

        var userMappingData=data;
        var d;

        $.each(userMappingData.user_mappings, function(key, value)
        {
            if(logged_user_id==value.parent_user_id)
            {
                DOMAINEXECUTIVES.push(value.child_user_id);
                childUsersDetails(ALLUSERINFO, logged_user_id, value.child_user_id)
            }
        });

    }
    function childUsersDetails(ALLUSERINFO, parent_user_id, child_user_id)
    {

        $.each(ALLUSERINFO, function(key, value)
        {

           if($.inArray(parseInt(child_user_id), EXISTINGUSERID)==-1)
           {

             if(child_user_id==value["user_id"]
                && value["is_active"]==true)
             {

                var option = $('<option></option>');
                option.val(value["user_id"]);
                option.text(value["employee_code"]+" - "+value["employee_name"]);

                $('#dename-dmanager').append(option);
                EXISTINGUSERID.push(parseInt(child_user_id));
             }
            }
        });
        $('#dename-dmanager').multiselect('rebuild');
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

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'group-id'){
      resetfilter('clients');
    }else if(current_id == 'businessgroupid'){
      resetfilter('bg');
    }
    else if(current_id == 'legalentityid'){
      resetfilter('le');
    }else if(current_id == 'unitid'){
      resetfilter('unit');
    }
}

//load group form list in autocomplete text box
$('#groupsval').keyup(function (e) {
  resetfilter('clients');
  var textval = $(this).val();
  var ctry_grps=[];
  /*if($('#country-id').val() > 0)
  {*/
    for(var i=0;i<CLIENTLIST.length;i++)
    {
      if(CLIENTLIST[i].country_id)
      {
        var occur = -1
        for(var j=0;j<ctry_grps.length;j++){
          if(ctry_grps[j].client_id == CLIENTLIST[i].client_id){
            occur = 1;
            break;
          }
        }
        if(occur < 0){
          ctry_grps.push({
            "client_id": CLIENTLIST[i].client_id,
            "group_name": CLIENTLIST[i].client_name,
            "is_active": true
          });
        }

      }
    }
    commonAutoComplete(
        e, ACGroup, Group, textval,
        ctry_grps, "group_name", "client_id", function (val) {
          onAutoCompleteSuccess(GroupVal, Group, val);
    });

});


//load legalentity form list in autocomplete text box
LegalEntityVal.keyup(function (e) {
  resetfilter('le');
  var textval = $(this).val();
  var le_list = [];
  var client_id = Group.val();
  var bgrp_id = $('#businessgroupid').val();
  if(Group.val() > 0)
  {
    var condition_fields = [];
    var condition_values = [];
    if(Group.val() != ''){
      condition_fields.push("client_id");
      condition_values.push(Group.val());
    }
    for(var i =0; i < CLIENTLIST.length; i++)
    {
      var bg_check = bgrp_id > 0 ? (bgrp_id === CLIENTLIST[i].business_group_id):false;
      if((CLIENTLIST[i].client_id == client_id) &&
        (bg_check == true || bg_check == false))
      {
        for(var j = 0; j < legelEntityList.length; j++)
        {
          if(legelEntityList[j].legal_entity_id == CLIENTLIST[i].legal_entity_id)
          {
            le_list.push({
              "client_id": CLIENTLIST[i].client_id,
              "business_group_id": legelEntityList[j].business_group_id,
              "legal_entity_id": legelEntityList[j].legal_entity_id,
              "legal_entity_name": legelEntityList[j].legal_entity_name
            });
          }
        }
      }
    }
    commonAutoComplete(
      e, ACLegalEntity, LegalEntity, textval,
      le_list, "legal_entity_name", "legal_entity_id", function (val) {
          onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
          loadDomains();
      }, condition_fields, condition_values);
  }

});

Domain.on('change', function(e) {
     resetfilter('domains');
  });

//load legalentity form list in autocomplete text box
UnitVal.keyup(function (e) {
  resetfilter('unit');
  var textval = $(this).val();
  var unit_list = [];
  var client_id = Group.val();
  var le_id = $('#legalentityid').val();
  var domain_ids = Domain.val();
  var unit_code_name;

  var selectedDomain=[];
   $.each(domain_ids, function(key, value){
        selectedDomain.push(parseInt(value));
   });

  if(client_id > 0 && le_id > 0)
  {
    for(var i =0; i < ASSIGNEDUNITLIST.length; i++)
    {
      if(ASSIGNEDUNITLIST[i].client_id == client_id
        && ASSIGNEDUNITLIST[i].legal_entity_id == le_id
        && $.inArray(ASSIGNEDUNITLIST[i].d_id, selectedDomain) >= 0)
      {
        unit_code_name=ASSIGNEDUNITLIST[i].unit_code_name;
        unit_code=unit_code_name.split("-");
        unit_code=unit_code[0];

        unit_list.push({
          "unit_id": unit_code,
          "unit_name": ASSIGNEDUNITLIST[i].unit_code_name
        });
      }
    }
    commonAutoComplete(
      e, ACUnit, Unit, textval,
      unit_list, "unit_name", "unit_id", function (val) {
          onAutoCompleteSuccess(UnitVal, Unit, val);
    });
  }

});
function AssignStatutoryBulkReport() {}

// Fields Manadory validation
AssignStatutoryBulkReport.prototype.validateMandatory = function()
{
    is_valid = true;

    if (Group.val().trim().length == 0)
    {
        displayMessage(message.clientgroup_required);
        is_valid = false;
    }
    else if (LegalEntity.val().trim().length == 0)
    {
        displayMessage(message.legalentity_required);
        is_valid = false;
    }
    else if ($('#domain option:selected').text() == "")
    {
        displayMessage(message.domain_required);
        is_valid = false;
    }
    else if (FROMDATE.val().trim() == "")
    {
        displayMessage(message.fromdate_required);
        is_valid = false;
    }
    else if (TODATE.val().trim() == "")
    {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};

AssignStatutoryBulkReport.prototype.pageControls=function() {

    SHOW_BTN.click(function() {
        is_valid = s_page.validateMandatory();
        if (is_valid == true)
        {
            s_page._ON_CURRENT_PAGE = 1;
            s_page._total_record = 0;

            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
            });

            ON_CURRENT_PAGE = 1;
            processSubmit();
         }
    });

    ITEMSPERPAGE.on('change', function(e) {
        perPage = parseInt($(this).val());
        SNO = 0;
        ON_CURRENT_PAGE = 1;
        createPageView(TOTALRECORD);
        processSubmit();
    });

    EXPORT_BTN.click(function(e) {
        is_valid = s_page.validateMandatory();
        if (is_valid == true) {
            CSV = true;
            s_page.exportData();
        }
    });

}
function loadDomains() {

    /******** Load Domain Lists *********/

    var client_id = Group.val();
    var legal_id = LegalEntity.val();
    var APIClientID;
    var APILegalEntityID;
    var countriesList=[];


    $.each(CLIENTLIST, function(key, value)
    {
      APIClientID=parseInt(value["client_id"]);
      APILegalEntityID=parseInt(value["legal_entity_id"]);

      if(client_id==APIClientID && legal_id==APILegalEntityID)
      {
        countriesList.push(parseInt(value["country_id"]));

      }
    });
    getDomainByCountryID(countriesList);
}
function getDomainByCountryID(countriesList)
{       var sText = '';
        var str='';
        $.each(countriesList, function(key, countryId)
        {
            var cId = countryId;
            var flag = true;

            $.each(DomainList, function(key1, v)
            {
                if (v.is_active == false)
                {
                    return;
                }
                if($.inArray(cId, v.country_ids) >= 0)
                {
                    var dVal = v.domain_id;
                    str += '<option value="' + dVal + '" ' + sText + '>' + v.domain_name + '</option>';
                    flag = false;
                }
            });

        });
        $('#domain').append(str);
        $('#domain').multiselect('rebuild');
}
// get statutory mapping report data from api
function processSubmit() {
    var clientGroup = parseInt(Group.val());
    var legalEntityID = parseInt(LegalEntity.val());
    var deIds = DENAME.val();
    var domain_ids = Domain.val();
    var unitID="";

    var fromDate = FROMDATE.val();
    var toDate = TODATE.val();

    var selectedDEName=[];
    var splitValues;

    var selectedDomain=[];
    $.each(domain_ids, function(key, value){
        selectedDomain.push(parseInt(value));
    });

     if(Unit.val()){
       unitID=Unit.val();
     }


     /* multiple COUNTRY selection in to generate array */
     if($('#dename-dmanager option:selected').text()== ""){
        selectedDEName=EXISTINGUSERID;  // When execute unselected the Field.
     }
     else{
      $.each(deIds, function(key, value){
       selectedDEName.push(parseInt(value));
      });
     }

        displayLoader();
        _page_limit = parseInt(ITEMSPERPAGE.val());

        if (ON_CURRENT_PAGE == 1) {
            SNO = 0
        } else {
            SNO = (ON_CURRENT_PAGE - 1) * _page_limit;
        }

        filterdata = {
            "bu_client_id":clientGroup,
            "bu_legal_entity_id":legalEntityID,
            "bu_unit_id":unitID,
            "domain_ids":selectedDomain,
            "from_date": fromDate,
            "to_date" : toDate,
            "r_count" : SNO,
            "p_count" : _page_limit,
            "child_ids" : selectedDEName,
            "user_category_id" : UserCategoryID
        };
        function onSuccess(data) {

            $('.details').show();
            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
                $(this).show();
            });


            SNO = SNO;
            assignStatutoryData = data.assign_statutory_data;
            TOTALRECORD=data.total;
            hideLoader();

            if (TOTALRECORD == 0) {
                $('.tbody-compliance').empty();
                var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
                var clone4 = tableRow4.clone();
                $('.tbl_norecords', clone4).text('No Records Found');
                $('.tbody-compliance').append(clone4);
                PAGINATIONVIEW.hide();
                ReportView.show();
                hideLoader();
            } else {
                hideLoader();
                if (SNO == 0) {
                    createPageView(TOTALRECORD);
                }
                PAGINATIONVIEW.show();
                ReportView.show();
                loadCountwiseResult(assignStatutoryData);
            }

        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }

        bu.getAssignedStatutoryBulkReportData(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
        //temp_act = act;
    //}
}
//display statutory mapping details accoring to count
function loadCountwiseResult(filterList) {
    $('.tbody-compliance').empty();
    lastActName = '';
    lastOccuranceid = 0;
    var showFrom = SNO + 1;
    var is_null = true;

    for (var entity in filterList) {

        is_null = false;

        SNO = parseInt(SNO) + 1;


        var domain = filterList[entity].domain;
        //alert(domain);
        var csv_name = filterList[entity].csv_name;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var uploaded_by = filterList[entity].uploaded_by;
        var uploaded_on = filterList[entity].uploaded_on;
        var total_rejected_records = filterList[entity].total_rejected_records;
        var rejected_on = filterList[entity].rejected_on;
        var rejected_by = filterList[entity].rejected_by;
        var reason_for_rejection = filterList[entity].is_fully_rejected;
        var total_approve_records = filterList[entity].total_approve_records;
        var rejected_reason = filterList[entity].rejected_reason;
        var domain_name = filterList[entity].domain_name;
        var approved_on = filterList[entity].approved_on;
        var approved_by = filterList[entity].approved_by;
        approved_rejected_on = '';
        approved_rejected_by = '';
        approved_rejected_tasks = '-';




        $(ALLUSERINFO).each(function(key,value)
        {
            if(parseInt(uploaded_by)==value["user_id"])
            {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                uploaded_by=EmpCode+" - "+ EmpName.toUpperCase();
            }
            else if(parseInt(rejected_by)==value["user_id"])
            {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                rejected_by=EmpCode+" - "+ EmpName.toUpperCase();
            }
            else if(parseInt(approved_by)==value["user_id"])
            {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                approved_by=EmpCode+" - "+ EmpName.toUpperCase();
            }
        });

        if (parseInt(reason_for_rejection) == 1) {
            reason_for_rejection = rejected_reason;
        } else {
            reason_for_rejection = "";
            approved_rejected_tasks =  total_approve_records;
            approved_rejected_tasks += " / ";
            approved_rejected_tasks += total_rejected_records;
        }

        if (String(approved_on) != null && String(approved_on) != '') {
            approved_rejected_on = approved_on;
            approved_rejected_by = approved_by;
        }
        else if (String(rejected_on) != null && String(rejected_on) != '') {
            approved_rejected_on = rejected_on;
            approved_rejected_by = rejected_by;
        }

        var occurance = '';
        var occuranceid;
        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();

        $('.tbl_sno', clone1).text(SNO);
        $('.tbl_uploaded_file_name', clone1).text(csv_name);
        $(".tbl_uploaded_by", clone1).text(uploaded_by);
        $('.tbl_uploaded_on', clone1).text(uploaded_on);
        $('.tbl_no_of_tasks', clone1).text(tbl_no_of_tasks);
        $('.tbl_approved_rejected_tasks', clone1).text(approved_rejected_tasks);
        $('.tbl_approved_rejected_on', clone1).text(approved_rejected_on);
        $('.tbl_approved_rejected_by', clone1).text(approved_rejected_by);
        $('.tbl_reason_for_rejection', clone1).text(reason_for_rejection);
        $('.tbl_domain', clone1).text(domain_name);
        $('#datatable-responsive .tbody-compliance').append(clone1);
    }

    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, SNO, TOTALRECORD);
    }
    hideLoader();
}


$(function () {
  $('.grid-table-rpt').hide();
  s_page.pageControls();
  initialize();
  UserGroupDetails();
  ITEMSPERPAGE.on('change', function (e) {
    perPage = parseInt($(this).val());
      SNO = 0;
      ON_CURRENT_PAGE = 1;
      $('#show-button').trigger( "click" );
  });
  loadItemsPerPage();
});

//To export data
AssignStatutoryBulkReport.prototype.exportData = function() {

    var clientGroup = parseInt(Group.val());
    var clientGroupName = GroupVal.val();
    var legalEntityID = parseInt(LegalEntity.val());
    var legalEntityName = LegalEntityVal.val();
    var deIds = DENAME.val();
    var domain_ids = Domain.val();
    var unitID = "";
    var unitName = UnitVal.val();

    var fromDate = FROMDATE.val();
    var toDate = TODATE.val();

    var selectedDEName=[];
    var splitValues;

    var selectedDomain=[];
    $.each(domain_ids, function(key, value){
        selectedDomain.push(parseInt(value));
    });

     if(Unit.val()){
       unitID=Unit.val();
     }


     /* multiple COUNTRY selection in to generate array */
     if($('#dename-dmanager option:selected').text()== ""){
        selectedDEName = EXISTINGUSERID;  // When execute unselected the Field.
     }
     else{
      $.each(deIds, function(key, value){
       selectedDEName.push(parseInt(value));
      });
     }

    var domainNames = $("#domain option:selected").map(function () {
        return $(this).text();
    }).get().join(',');

      displayLoader();

      filterdata = {
          "bu_client_id":clientGroup,
          "bu_group_name": clientGroupName,
          "bu_legal_entity_id":legalEntityID,
          "legal_entity_name": legalEntityName,
          "bu_unit_id":unitID,
          "unit_name": unitName,
          "domain_ids":selectedDomain,
          "d_names": domainNames,
          "from_date": fromDate,
          "to_date" : toDate,
          "child_ids" : selectedDEName,
          "user_category_id" : UserCategoryID,
          "csv": CSV
      };

    displayLoader();
    bu.exportASBulkReportData(filterdata,
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
