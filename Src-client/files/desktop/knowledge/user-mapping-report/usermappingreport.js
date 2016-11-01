var countriesList;
var clientList;
var businessGroupList;
var lagelEntityList;
var divisionList;
var categoryList;
var assignedUnitList;
var prev_country_id, prev_client_id, prev_bg_id, prev_le_id, prev_divi_id, prev_catg_id, prev_unit_id;
function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

//load all the filters
function initialize() {
  console.log("inside data");
  function onSuccess(data) {
    countriesList = data.countries;
    clientList = data.usermapping_groupdetails;
    businessGroupList = data.usermapping_business_groups;
    lagelEntityList = data.usermapping_legal_entities;
    divisionList = data.usermapping_unit;
    categoryList = data.usermapping_unit;
    assignedUnitList = data.usermapping_unit;
    console.log(data);
    resetallfilter();
    loadCountries(countriesList);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getUserMappingReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

//load countries
function loadCountries(countriesList)
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
  var country_id = $('#countries').val();
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
}

function resetfilter(evt)
{
  //alert("jhjh");'
  console.log(evt);
  if(evt == 'countries')
  {
    $('#clientids').find('option').not(':first').remove();
    $('#businessgroup').find('option').not(':first').remove();
    $('#legalentity').find('option').not(':first').remove();
    $('#division').find('option').not(':first').remove();
    $('#category').find('option').not(':first').remove();
    $('#units').find('option').not(':first').remove();
  }
  if(evt == 'clients')
  {
    $('#businessgroup').find('option').not(':first').remove();
    $('#legalentity').find('option').not(':first').remove();
    $('#division').find('option').not(':first').remove();
    $('#category').find('option').not(':first').remove();
    $('#units').find('option').not(':first').remove();
  }
  if(evt == 'bg')
  {
    //$('#businessgroup').find('option').not(':first').remove();
    $('#legalentity').find('option').not(':first').remove();
    $('#division').find('option').not(':first').remove();
    $('#category').find('option').not(':first').remove();
    $('#units').find('option').not(':first').remove();
  }
  if(evt == 'le')
  {
    //$('#businessgroup').find('option').not(':first').remove();
    //$('#legalentity').find('option').not(':first').remove();
    $('#division').find('option').not(':first').remove();
    $('#category').find('option').not(':first').remove();
    $('#units').find('option').not(':first').remove();
  }
  if(evt == 'divi')
  {
    //$('#businessgroup').find('option').not(':first').remove();
    //$('#legalentity').find('option').not(':first').remove();
    //$('#division').find('option').not(':first').remove();
    $('#category').find('option').not(':first').remove();
    $('#units').find('option').not(':first').remove();
  }
  if(evt == 'catg')
  {
    //$('#businessgroup').find('option').not(':first').remove();
    //$('#legalentity').find('option').not(':first').remove();
    //$('#division').find('option').not(':first').remove();
    //$('#category').find('option').not(':first').remove();
    $('#units').find('option').not(':first').remove();
  }
}

$('#show-button').click(function () {
  alert("show")
  sno = 0;
  lastBG = '';
  lastLE = '';
  lastDv = '';
  $('.table-usermappingdeytails-list tbody').empty();
  loadusermappingdetails();
});

function loadusermappingdetails() {
  clearMessage();
  var country_id = $('#countries').val();
  var client_id = $('#clientids').val();
  var bgrp_id = $('#businessgroup').val();
  var le_id = $('#legalentity').val();
  var divi_id = $('#division').val();
  var catg_id = $('#category').val();

  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    function onSuccess(data) {
      console.log("success")
      console.log(data);
      $('.grid-table-rpt').show();
      /*$('.countryval').text(countriesText);
      $('.groupsval').text(groupsval);
      totalRecord = data.total_count;*/
      loadUserMappingDetailsList(data);
    }
    function onFailure(error) {
      displayMessage(error);
    }
    mirror.getUsermappingDetailsReport(parseInt(country_id), parseInt(client_id), parseInt(le_id), function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
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
    if(le_id  == 0 || le_id == '')
    {
      displayMessage(message.legal_entity_required);
    }
  }
}

function loadUserMappingDetailsList(data)
{
  var th_cnt=3;
  var sno = 0;
  domainsList = data.domains;

  var country_name = $('#countries  option:selected').text();
  var client_name = $('#clientids  option:selected').text();
  var business_group_name = $('#businessgroup  option:selected').text();
  var legal_entity_name = $('#legalentity  option:selected').text();
  var divi_name = $('#division  option:selected').text();
  var category_name = $('#category  option:selected').text();

  /*var tablefilter = $('#templates .tr-filter');
  var clonefilter = tablefilter.clone();
  $('.countryval', clonefilter).text(country_name);
  $('.groupsval', clonefilter).text(client_name);
  $('.bgroupsval', clonefilter).text(business_group_name);
  $('.lentityval', clonefilter).text(legal_entity_name);
  $('.divisionval', clonefilter).text(divi_name);
  $('.categoryval', clonefilter).text(category_name);*/
  //$('.tbody-usermappingdetails-list').append(clonefilter);
  var tableheading = $('#templates .tr-heading');
  var cloneheading = tableheading.clone();
  $('.tbody-usermappingdetails-list').append(cloneheading);
  if(domainsList.length > 0)
  {
    for(var i=0;i<domainsList.length;i++)
    {
      $('.tbody-usermappingdetails-list tr :last-child').each(function() {
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
          th_cnt++;
        }
      });
    }
  }

  //load details
  technoDetails = data.techno_details;
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
      var headerObj = $('.tbody-usermappingdetails-list').find('th').eq(k);
      getDomainVal = getDomainAssigned(headerObj.text(), technoDetails[i].unit_id, data);
      if(assignedDomainVal == '')
      {
        assignedDomainVal  = getDomainVal;
      }
      else
      {
        assignedDomainVal  = assignedDomainVal +"," + getDomainVal;
      }
      console.log("val:"+assignedDomainVal)
    }
    if(assignedDomainVal_1 == '')
    {
      assignedDomainVal_1  = assignedDomainVal;
    }
    else
    {
      assignedDomainVal_1  = assignedDomainVal_1 +";"+assignedDomainVal;
    }
    console.log("val_!:"+assignedDomainVal_1);

  }

  var split_domain_with_colon = assignedDomainVal_1.split(";");


  $('.tbody-usermappingdetails-list tr :last-child').each(function() {
    var index = $(this).closest('tr').index();
    //alert("indx:"+index)
    if(index > 0)
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
  });

  if(sno == 0)
  {
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No record Found');
    $('.tbody-usermappingdetails-list').append(clone4);
  }
  else
  {
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('Total Records :'+sno);
    $('.tbody-usermappingdetails-list').append(clone4);
  }
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