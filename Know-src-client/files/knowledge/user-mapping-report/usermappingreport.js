var countriesList;
var clientList;
var businessGroupList;
var lagelEntityList;
var divisionList;
var categoryList;
var assignedUnitList;
var mappedUserList;
var userMappingList;
var prev_country_id, prev_client_id, prev_bg_id, prev_le_id, prev_divi_id, prev_catg_id, prev_unit_id;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACUnit = $('#ac-unit');
var ACDivision = $('#ac-division');
var ACCategory = $('#ac-category');

//Input field variable declaration
var CountryVal = $('#countryval');
var Country = $('#country-id');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var BusinessGroupVal = $('#businessgroupsval');
var BusinessGroup = $('#businessgroupid');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');
var UnitVal = $('#unitval');
var Unit = $('#unitid');
var DivisionVal = $('#divisionval');
var Division = $('#divisionid');
var CategoryVal = $('#categoryval');
var Category = $('#categoryid');

var SubmitButton = $('#show-button');
var ExportButton = $('#export');
var csv = false;

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var _page_limit = 25;
var totalRecord;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

//load all the filters
function initialize() {
  function onSuccess(data) {
    countriesList = data.countries;
    clientList = data.usermapping_groupdetails;
    businessGroupList = data.usermapping_business_groups;
    legelEntityList = data.usermapping_legal_entities;
    divisionList = data.usermapping_unit;
    categoryList = data.usermapping_unit;
    assignedUnitList = data.usermapping_unit;
    console.log(data)
    resetAllfilter();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getUserMappingReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
      hideLoader();
    } else {
      onFailure(error);
      hideLoader();
    }
  });
}

//load countries
/*function loadCountries(countriesList)
{
  $('#countries').focus();
  var countries = countriesList;

  for(var i =  0; i < countries.length; i++)
  {
    var obj = $(".country-drop-down option");
    var clone = obj.clone();
    clone.attr("value", countries[i].country_id);
    clone.text(countries[i].country_name);
    $('#countries').append(clone);
  }
}

//load client groups
function loadClientGroups()
{
  console.log($('#clientids').length);
  console.log("country:"+$('#countries').val());
  var country_id = $('#countries').val();
  prev_country_id = country_id;
  if(country_id > 0)
  {
    //if($('#clientids').length > 1)
    $('#clientids').find('option').not(':first').remove();
    for(var i = 0; i < clientList.length; i++)
    {
      if(clientList[i].country_id == country_id)
      {
        var obj = $(".client-drop-down option");
        var clone = obj.clone();
        clone.attr("value", clientList[i].client_id);
        clone.text(clientList[i].client_name);
        $('#clientids').append(clone);
      }
    }
  }
  else
  {
    displayMessage(message.country_required);
  }
  resetfilter('clients');
}

//load Business groups
function loadBusinessGroup()
{
  console.log("Client:"+$('#clientids').val());
  var country_id = $('#country-id').val();
  var client_id = $('#clientids').val();
  prev_client_id = client_id;
  if((client_id > 0) && (country_id > 0))
  {
    $('#businessgroup').find('option').not(':first').remove();
    for(var i =0; i < clientList.length; i++)
    {
      if(clientList[i].country_id == country_id && clientList[i].client_id == client_id)
      {
        for(var j = 0; j < businessGroupList.length; j++)
        {
          if(businessGroupList[j].business_group_id == clientList[i].business_group_id)
          {
            var obj = $(".bgrp-drop-down option");
            var clone = obj.clone();
            clone.attr("value", businessGroupList[j].business_group_id);
            clone.text(businessGroupList[j].business_group_name);
            $('#businessgroup').append(clone);
          }
        }
      }
    }
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
  }
  resetfilter('bg');
}

//load legal entity'
function loadLegalEntity()
{
  console.log("Client:"+$('#clientids').val());
  var country_id = $('#countries').val();
  var client_id = $('#clientids').val();
  var bgrp_id = $('#businessgroup').val();
  prev_bg_id = bgrp_id;
  if((client_id > 0) && (country_id > 0))
  {
    $('#legalentity').find('option').not(':first').remove();
    for(var i =0; i < clientList.length; i++)
    {
      if((clientList[i].country_id == country_id && clientList[i].client_id == client_id))
      {
        console.log("inside le loop")
        for(var j = 0; j < lagelEntityList.length; j++)
        {
          if(lagelEntityList[j].legal_entity_id == clientList[i].legal_entity_id)
          {
            var obj = $(".le-drop-down option");
            var clone = obj.clone();
            clone.attr("value", lagelEntityList[j].legal_entity_id);
            clone.text(lagelEntityList[j].legal_entity_name);
            $('#legalentity').append(clone);
          }
        }
      }
    }
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
  }
  resetfilter('le');
}

//load division
function loadDivision()
{
  var country_id = $('#countries').val();
  var client_id = $('#clientids').val();
  var bgrp_id = $('#businessgroup').val();
  var le_id = $('#legalentity').val();
  prev_le_id = le_id;
  if((client_id > 0) && (country_id > 0) && (le_id > 0))
  {
    $('#division').find('option').not(':first').remove();
    for(var i =0; i < divisionList.length; i++)
    {
      if((divisionList[i].country_id == country_id && divisionList[i].client_id == client_id && divisionList[i].legal_entity_id == le_id))
      //        (bgrp_id > 0 && divisionList[i].business_group_id == bgrp_id))
      {
        var obj = $(".divi-drop-down option");
        var clone = obj.clone();
        clone.attr("value", divisionList[i].division_id);
        clone.text(divisionList[i].division_name);
        $('#division').append(clone);
      }
    }
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legal_entity_required);
    }
  }
  resetfilter('divi');
}

//load category
function loadCategory()
{
  var country_id = $('#countries').val();
  var client_id = $('#clientids').val();
  var bgrp_id = $('#businessgroup').val();
  var le_id = $('#legalentity').val();
  var divi_id = $('#division').val();
  prev_divi_id = divi_id;
  if((client_id > 0) && (country_id > 0) && (le_id > 0))
  {
    $('#category').find('option').not(':first').remove();
    for(var i =0; i < categoryList.length; i++)
    {
      if((categoryList[i].country_id == country_id && categoryList[i].client_id == client_id && categoryList[i].legal_entity_id == le_id) ||
        (bgrp_id > 0 && categoryList[i].business_group_id == bgrp_id) ||
          (divi_id > 0 && categoryList[i].division_id == divi_id))
      {
        var obj = $(".catg-drop-down option");
        var clone = obj.clone();
        clone.attr("value", categoryList[i].category_id);
        clone.text(categoryList[i].category_name);
        $('#category').append(clone);
      }
    }
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legal_entity_required);
    }
  }
  resetfilter('catg');
}

//load assigned units
function loadAssignedUnits()
{
  var country_id = $('#countries').val();
  var client_id = $('#clientids').val();
  var bgrp_id = $('#businessgroup').val();
  var le_id = $('#legalentity').val();
  var divi_id = $('#division').val();
  var catg_id = $('#category').val();
  prev_catg_id = catg_id;
  if((client_id > 0 ) && (country_id > 0) && (le_id > 0))
  {
    $('#units').find('option').not(':first').remove();
    for(var i =0; i < assignedUnitList.length; i++)
    {
      if((assignedUnitList[i].country_id == country_id && assignedUnitList[i].client_id == client_id && assignedUnitList[i].legal_entity_id == le_id) ||
        (bgrp_id > 0 && assignedUnitList[i].business_group_id == bgrp_id) ||
          (divi_id > 0 && assignedUnitList[i].division_id == divi_id) ||
            (catg_id > 0 && assignedUnitList[i].category_id == catg_id))
      {
        var obj = $(".units-drop-down option");
        var clone = obj.clone();
        clone.attr("value", assignedUnitList[i].unit_id);
        clone.text(assignedUnitList[i].unit_code_name);
        $('#units').append(clone);
      }
    }
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legal_entity_required);
    }
  }
  r//esetfilter('clients');
}

function resetallfilter()
{
  var obj_ctry = $(".country-drop-down option");
  var clone_ctry = obj_ctry.clone();
  clone_ctry.attr("value", 0);
  clone_ctry.text("Select");
  $('#countries').append(clone_ctry);

  var obj_client = $(".client-drop-down option");
  var clone_client = obj_client.clone();
  clone_client.attr("value", 0);
  clone_client.text("Select");
  $('#clientids').append(clone_client);

  var obj_bgrp = $(".bgrp-drop-down option");
  var clone_bgrp = obj_bgrp.clone();
  clone_bgrp.attr("value", 0);
  clone_bgrp.text("Select");
  $('#businessgroup').append(clone_bgrp);

  var obj_le = $(".le-drop-down option");
  var clone_le = obj_le.clone();
  clone_le.attr("value", 0);
  clone_le.text("Select");
  $('#legalentity').append(clone_le);

  var obj_divi = $(".divi-drop-down option");
  var clone_divi = obj_divi.clone();
  clone_divi.attr("value", 0);
  clone_divi.text("Select");
  $('#division').append(clone_divi);

  var obj_catg = $(".catg-drop-down option");
  var clone_catg = obj_catg.clone();
  clone_catg.attr("value", 0);
  clone_catg.text("Select");
  $('#category').append(clone_catg);

  var obj_units = $(".units-drop-down option");
  var clone_units = obj_units.clone();
  clone_units.attr("value", 0);
  clone_units.text("Select");
  $('#units').append(clone_units);
}*/

function resetAllfilter()
{
  $('#countryval').val('');
  $('#groupsval').val('');
  $('#businessgroupsval').val('');
  $('#legalentityval').val('');
  $('#divisionval').val('');
  $('#categoryval').val('');
  $('#unitval').val('');
  $('.tbody-usermappingdetails-list').empty();
  $('#countryval').focus();
}
function resetfilter(evt)
{
  if(evt == 'countries')
  {
    $('#groupsval').val('');
    $('#businessgroupsval').val('');
    $('#legalentityval').val('');
    $('#divisionval').val('');
    $('#categoryval').val('');
    $('#unitval').val('');
  }
  if(evt == 'clients')
  {
    $('#businessgroupsval').val('');
    $('#legalentityval').val('');
    $('#divisionval').val('');
    $('#categoryval').val('');
    $('#unitval').val('');
  }
  if(evt == 'bg')
  {
    $('#legalentityval').val('');
    $('#divisionval').val('');
    $('#categoryval').val('');
    $('#unitval').val('');
  }
  if(evt == 'le')
  {
    $('#divisionval').val('');
    $('#categoryval').val('');
    $('#unitval').val('');
  }
  if(evt == 'divi')
  {
    $('#categoryval').val('');
    $('#unitval').val('');
  }
  if(evt == 'catg')
  {
    $('#unitval').val('');
  }

  $('.tbody-usermappingdetails-list').empty();
  $('.grid-table-rpt').hide();
}

ExportButton.click(function() {
  //alert("x");
    if(mappedUserList.length > 0){
      csv = true;
      sno = 0;
      loadusermappingdetails();
    }
    else{
      displayMessage(message.export_empty);
    }

});
$('#show-button').click(function () {
  sno = 0;
  lastBG = '';
  lastLE = '';
  lastDv = '';
  csv = false;
  $('.details').show();
  $('#compliance_animation')
    .removeClass().addClass('bounceInLeft animated')
    .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
    $(this).removeClass();
  });
  $('.tbody-usermappingdetails-list').empty();
  loadusermappingdetails();
});

//pagination - functions
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
}

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
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                processPaging();
            }
        }
    });
};

function processPaging(){
  _page_limit = parseInt(ItemsPerPage.val());
  if (on_current_page == 1) {
    sno = 0
  }
  else {
    sno = (on_current_page - 1) *  _page_limit;
  }
  sno  = sno;
  totalRecord = mappedUserList.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.tbody-usermappingdetails-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-usermappingdetails-list').append(clone4);
    ExportButton.hide();
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      ExportButton.show();
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadUserMappingDetailsList(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<mappedUserList.length;i++)
  {
    is_null = false;
    data.push(mappedUserList[i]);
    if(i == (recordLength-1))
    {
      break;
    }
  }
  if (is_null == true) {
    hidePagePan();
  }
  else {
    if(recordLength < totalRecord)
      showPagePan(showFrom, recordLength, totalRecord);
    else
      showPagePan(showFrom, totalRecord, totalRecord);
  }
  return data;
}

function loadusermappingdetails() {
  clearMessage();
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var divi_id = $('#divisionid').val();
  var catg_id = $('#categoryid').val();
  var unit_id = $('#unitid').val();
  var null_values = "";

  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    if($('#businessgroupid').val() == '')
    {
      bgrp_id = 0;
    }
    if($('#divisionid').val() == "")
    {
      divi_id = 0;
    }
    if($('#categoryid').val() == "")
    {
      catg_id = 0;
    }
    if($('#unitid').val() == "")
    {
      unit_id = 0;
    }
    null_values = bgrp_id + "," + divi_id + "," + catg_id + "," + unit_id;


    if (on_current_page == 1) {
        sno = 0
    } else {
        sno = (on_current_page - 1) * _page_limit;
    }

    function onSuccess(data) {
      console.log(data);
      if (csv) {
          var download_url = data.link;
          window.open(download_url, '_blank');
      }else{
        $('.grid-table-rpt').show();
        mappedUserList = data.techno_details;
        userMappingList = data;
        totalRecord = data.techno_details.length;
        //loadUserMappingDetailsList(data);
        processPaging();
      }
    }
    function onFailure(error) {
      displayMessage(error);
    }
    displayLoader();
    mirror.getUsermappingDetailsReport(parseInt(country_id), parseInt(client_id), parseInt(le_id), null_values,
      csv, sno, _page_limit,
      function (error, response) {
      if (error == null) {
        onSuccess(response);
        hideLoader();
      } else {
        onFailure(error);
        hideLoader();
      }
    });
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    else if(le_id  == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }
  }
}

function loadUserMappingDetailsList(data)
{
  var th_cnt=3;
  var sno = 0;
  $('.tbody-usermappingdetails-list').empty();
  $('.usermapping-header').empty();
  //$('.#datatable-responsive').empty();
  domainsList = userMappingList.usermapping_domain;
  var country_name = $('#countryval').val();
  var client_name = $('#groupsval').val();
  var business_group_name = $('#businessgroupsval').val();
  var legal_entity_name = $('#legalentityval').val();
  var divi_name = $('#divisionval').val();
  var category_name = $('#categoryval').val();

  //load search details
  $('.countryval').text(country_name);
  $('.groupsval').text(client_name);
  if(business_group_name != "")
    $('.bgroupsval').text(business_group_name);
  else
    $('.bgroupsval').text(" - ");
  $('.lentityval').text(legal_entity_name);
  if(divi_name != "")
    $('.divisionval').text(divi_name);
  else
    $('.divisionval').text(" - ");

  if(category_name != "")
    $('.categoryval').text(category_name);
  else
    $('.categoryval').text(" - ");

  //$('#datatable-responsive th').remove();

  var tableheading = $('#templates .tr-heading');
  var cloneheading = tableheading.clone();
  $('.usermapping-header').append(cloneheading);


  if(domainsList.length > 0)
  {
    for(var i=0;i<domainsList.length;i++)
    {
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
  technoDetails = data;
  var assignedDomainVal = '';
  var assignedDomainVal_1 = '';
  var getDomainVal  = '';
  var col=4;
  for(var i=0;i<technoDetails.length;i++)
  {
    //alert(technoDetails.length);
    assignedDomainVal = '';
    var tableRow = $('#templates .table-row');
    var clone1 = tableRow.clone();
    sno = i + 1;

    $('.sno', clone1).text(sno);
    var unit_code_name = getUnitName(technoDetails[i].unit_id);
    $('.unit-name', clone1).text(unit_code_name);
    $('.techno-manager', clone1).text(technoDetails[i].techno_manager);
    $('.techno-user', clone1).text(technoDetails[i].techno_user);
    $('.tbody-usermappingdetails-list').append(clone1);

    for(var k=col;k<=th_cnt;k++)
    {
      var headerObj = $('#datatable-responsive').find('th').eq(k);
      getDomainVal = getDomainAssigned(headerObj.text(), technoDetails[i].unit_id, userMappingList);
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

  $('.tbody-usermappingdetails-list tr :last-child').each(function() {
    var index = $(this).closest('td').index();
    if(index > 0 && split_domain_with_colon.indexOf(";") > 0)
    {
      var split_domain_with_comma = split_domain_with_colon[index - 1].split(",");
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
    }
  });

}

function getDomainAssigned(domain_header, unit_id, data)
{
  unit_domains = data.unit_domains;
  var assignedDomainVal = "NA";
  for(var j=0;j<unit_domains.length;j++)
  {
    if(unit_domains[j].unit_id == unit_id)
    {
      var domain_name = getDomainName(unit_domains[j].domain_id);
      if(domain_header == (unit_domains[j].user_category_name+" "+domain_name))
      {
        assignedDomainVal = unit_domains[j].employee_name;
      }
    }
  }
  return assignedDomainVal;
}
function getUnitName(unit_id)
{
  var unit_code_name=null;
  for(var i =0; i < assignedUnitList.length; i++)
  {
    if(unit_id == assignedUnitList[i].unit_id)
    {
      unit_code_name = assignedUnitList[i].unit_code_name;
    }
  }
  return unit_code_name;
}

function getDomainName(domain_id)
{
  var domain_name = null;
  for(var i=0;i<domainsList.length;i++)
  {
    if(domain_id == domainsList[i].domain_id)
    {
      domain_name = domainsList[i].domain_name;
    }
  }
  return domain_name;
}

$(function () {
  $('.grid-table-rpt').hide();
  initialize();
  ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
      sno = 0;
      on_current_page = 1;
      createPageView(totalRecord);
      processPaging();
  });
  loadItemsPerPage();
});


//////////
 /*   for(var j=0;j<unit_domains.length;j++)
    {
      var col = 4;
      if(unit_domains[j].unit_id == technoDetails[i].unit_id)
      {
        var domain_name = getDomainName(unit_domains[j].domain_id);
        $('.tbody-usermappingdetails-list tr :last-child').each(function() {
          for(var k=col;k<=th_cnt;k++)
          {
            var headerObj = $('.tbody-usermappingdetails-list').find('th').eq(k);
            if(headerObj.text() == (unit_domains[j].user_category_name+" "+domain_name))
            {
              var clone2 = $(this).clone().html('&nbsp;');
              if (clone2.is('td')) {
                clone2.text(unit_domains[j].employee_name);
              }
              $(this).parent().append(clone2);
            }
            else
            {
              var clone2 = $(this).clone().html('&nbsp;');
              if (clone2.is('td')) {
                clone2.text("");
              }
              $(this).parent().append(clone2);
            }
          }
        });
      }
    }*/

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'country-id'){
      resetfilter('countries');
    }else if(current_id == 'group-id'){
      resetfilter('clients');
    }else if(current_id == 'businessgroupid'){
      resetfilter('bg');
    }
    else if(current_id == 'legalentityid'){
      resetfilter('le');
    }else if(current_id == 'unitid'){
      resetfilter('unit');
    }else if(current_id == 'divisionid'){
      resetfilter('divi');
    }
    else if(current_id == 'categoryid'){
      resetfilter('catg');
    }
}

//load country list in autocomplete textbox
$('#countryval').keyup(function (e) {
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACCountry, Country, text_val,
    countriesList, "country_name", "country_id", function (val) {
      onAutoCompleteSuccess(CountryVal, Country, val);
  });
});

//load group form list in autocomplete text box
$('#groupsval').keyup(function (e) {
  var textval = $(this).val();
  var ctry_grps=[];
  if($('#country-id').val() > 0)
  {
    for(var i=0;i<clientList.length;i++)
    {
      if(clientList[i].country_id == $('#country-id').val())
      {
        ctry_grps.push({
          "client_id": clientList[i].client_id,
          "group_name": clientList[i].client_name,
          "is_active": true
        });
      }
    }
    commonAutoComplete(
        e, ACGroup, Group, textval,
        ctry_grps, "group_name", "client_id", function (val) {
          onAutoCompleteSuccess(GroupVal, Group, val);
    });
  }
  /*else
  {
    displayMessage(message.country_required);
  }*/
});

//load businessgroup form list in autocomplete text box
$('#businessgroupsval').keyup(function (e) {
  var textval = $(this).val();
  var bg_grp = [];
  if($('#group-id').val() > 0)
  {
    var condition_fields = [];
    var condition_values = [];
    if(Group.val() != ''){
      condition_fields.push("client_id");
      condition_values.push(Group.val());
    }
    for(var i=0;i<clientList.length;i++)
    {
      if(clientList[i].client_id == $('#group-id').val() && clientList[i].country_id == $('#country-id').val())
      {
        for(var j=0;j<businessGroupList.length;j++)
        {
          if(businessGroupList[j].business_group_id == clientList[i].business_group_id)
          {
            bg_grp.push({
                "client_id": clientList[i].client_id,
                "business_group_id": businessGroupList[j].business_group_id,
                "business_group_name": businessGroupList[j].business_group_name
            });
            break;
          }
        }
      }
    }

    commonAutoComplete(
      e, ACBusinessGroup, BusinessGroup, textval,
      bg_grp, "business_group_name", "business_group_id", function (val) {
        onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
    }, condition_fields, condition_values);

  }
  /*else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }

  }*/
});

//load legalentity form list in autocomplete text box
$('#legalentityval').keyup(function (e) {
  var textval = $(this).val();
  var le_list = [];
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  if($('#group-id').val() > 0)
  {
    var condition_fields = [];
    var condition_values = [];
    if(Group.val() != ''){
      condition_fields.push("client_id");
      condition_values.push(Group.val());
    }
    for(var i =0; i < clientList.length; i++)
    {
      var bg_check = bgrp_id>0?(bgrp_id === clientList[i].business_group_id):false;
      if((clientList[i].country_id == country_id && clientList[i].client_id == client_id) &&
        (bg_check == true || bg_check == false))
      {
        for(var j = 0; j < legelEntityList.length; j++)
        {
          if(legelEntityList[j].legal_entity_id == clientList[i].legal_entity_id)
          {
            le_list.push({
              "client_id": clientList[i].client_id,
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
      }, condition_fields, condition_values);
  }
  /*else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }

  }*/
});

//load legalentity form list in autocomplete text box
$('#divisionval').keyup(function (e) {
  var textval = $(this).val();
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var division_list = [];
  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
   var condition_fields = [];
    var condition_values = [];
    if(Group.val() != ''){
      condition_fields.push("client_id");
      condition_values.push(Group.val());
    }
      condition_fields.push("legal_entity_id");
      condition_values.push(le_id);
    for(var i =0; i < divisionList.length; i++)
    {
      var bg_check = bgrp_id>0?(bgrp_id === divisionList[i].business_group_id):false;
      if(divisionList[i].country_id == country_id &&
        divisionList[i].client_id == client_id && divisionList[i].legal_entity_id == le_id
        && (bg_check == true || bg_check == false))
      //        (bgrp_id > 0 && divisionList[i].business_group_id == bgrp_id))
      {
        var occur = -1;
        for(var k=0;k<division_list.length;k++){
          if(division_list[k].division_id==divisionList[i].division_id){
            occur = 1;
          }
        }
        if(occur < 0){
          division_list.push({
            "client_id": divisionList[i].client_id,
            "legal_entity_id": divisionList[i].legal_entity_id,
            "division_id": divisionList[i].division_id,
            "division_name": divisionList[i].division_name
          });
        }

      }
    }
    commonAutoComplete(
      e, ACDivision, Division, textval,
      division_list, "division_name", "division_id", function (val) {
          onAutoCompleteSuccess(DivisionVal, Division, val);
      }, condition_fields, condition_values);
  }
  /*else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    else if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }
  }*/
});

//load legalentity form list in autocomplete text box
$('#categoryval').keyup(function (e) {
  var textval = $(this).val();
  var catg_list = [];
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var divi_id = $('#divisionid').val();
  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i =0; i < categoryList.length; i++)
    {
      var bg_check = bgrp_id>0?(bgrp_id === categoryList[i].business_group_id):false;
      var divi_check = divi_id>0?(divi_id === categoryList[i].division_id):false;
      if(categoryList[i].country_id == country_id &&
        categoryList[i].client_id == client_id && categoryList[i].legal_entity_id == le_id
        && (bg_check == true || bg_check == false) && (divi_check == true || divi_check == false))
      //        (bgrp_id > 0 && divisionList[i].business_group_id == bgrp_id))
      {
        var occur = -1;
        for(var k=0;k<catg_list.length;k++){
          if(catg_list[k].category_id==categoryList[i].category_id){
            occur = 1;
          }
        }
        if(occur < 0){
          catg_list.push({
            "category_id": categoryList[i].category_id,
            "category_name": categoryList[i].category_name
          });
        }

      }
    }
    commonAutoComplete(
      e, ACCategory, Category, textval,
      catg_list, "category_name", "category_id", function (val) {
          onAutoCompleteSuccess(CategoryVal, Category, val);
    });
  }
  /*else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    else if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }
  }*/
});

//load legalentity form list in autocomplete text box
$('#unitval').keyup(function (e) {
  var textval = $(this).val();
  var unit_list = [];
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var divi_id = $('#divisionid').val();
  var catg_id = $('#categoryid').val();
  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i =0; i < assignedUnitList.length; i++)
    {
      var bg_check = bgrp_id>0?(bgrp_id === assignedUnitList[i].business_group_id):false;
      var divi_check = divi_id>0?(divi_id === assignedUnitList[i].division_id):false;
      var catg_check = catg_id>0?(catg_id === assignedUnitList[i].category_id):false;
      if(assignedUnitList[i].country_id == country_id &&
        assignedUnitList[i].client_id == client_id && assignedUnitList[i].legal_entity_id == le_id
        && (bg_check == true || bg_check == false) && (divi_check == true || divi_check == false))
      //        (bgrp_id > 0 && divisionList[i].business_group_id == bgrp_id))
      {
        unit_list.push({
          "unit_id": assignedUnitList[i].unit_id,
          "unit_name": assignedUnitList[i].unit_code_name
        });
      }
    }
    commonAutoComplete(
      e, ACUnit, Unit, textval,
      unit_list, "unit_name", "unit_id", function (val) {
          onAutoCompleteSuccess(UnitVal, Unit, val);
    });
  }
  /*else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    else if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }
  }*/
});

