//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterDomain = $('#search-domain-name');
var FilterOrgn = $('#search-organization-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');/**
 * Created by Minds on 24/09/2016.
 */

var groupList;
var countryList;
var domainList;
var businessGroupList;
var legalEntitiesList;
var divisionList;
var countryFulList;
var countc = 1;
var industryList;
var unitList;
var geographyList;
var geographyLevelList;
var unitcodecount = 1001;
var countryByCount = 1;
var lastClassval = 1;
var unitcodeautogenerateids = null;
var get2CharsofGroup = null;
var max = {};
var auto_generate_initial_value = null;
var isUpdate = false;
var checkunitscount = null;
var usercountrycount = null;
var clientdomainList = null;
var division_cnt=0;
var unit_cnt=0;
var unit_values='';
var units_count = [];
var prev_org_id = 0;
var check_org = false;

var clientUnitAdd = $('#clientunit-add');
var clientUnitView = $('#clientunit-view');

//drop down in main search
var groupSelect_option_0 = $('#group-select  option:gt(0)');
var busgrpSelect_option_0 = $('#businessgroup-select  option:gt(0)');
var entitySelect_option_0 = $('#entity-select  option:gt(0)');
var groupSelect_option_no = $('#group-select option:not(:selected)');
var busgrpSelect_option_no = $('#businessgroup-select option:not(:selected)');
var entitySelect_option_no = $('#entity-select option:not(:selected)');

//main search filters
var clientSelect = $('#group-select');
var bgrpSelect = $('#businessgroup-select');
var leSelect = $('#entity-select');
var ctrySelect_name = $('#country-name');
var ctrySelect_id = $('#country-id');
var unitErrMsg = $('.unit-error-msg');

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterGroup = $('#search-group-name');
var FilterBGroup = $('#search-bgroup-name');
var FilterLE = $('#search-le-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var countryUnitList = $('.add-country-unit-list');

function initialize() {
  function onSuccess(data) {
    clientUnitAdd.hide();
    clientUnitView.show();
    isUpdate = false;
    countryByCount = 1;
    countc = 0;
    usercountrycount = 0;
    groupSelect_option_0.empty();
    busgrpSelect_option_0.empty();
    entitySelect_option_0.empty();
    console.log(data);
    groupList = data.group_company_list;
    businessGroupList = data.business_group_list;
    legalEntitiesList = data.unit_legal_entity;
    divisionList = data.divisions;
    countryFulList = data.countries_units;
    geographyLevelList = data.unit_geography_level_list;
    geographyList = data.unit_geographies_list;
    industryList = data.domains_organization_list;
    domainList = data.domains_organization_list;
    unitList = data.unit_list;
    //clientdomainList = data.client_domains;
    resetallfilter();
    loadClientsList(unitList);
  }
  function onFailure(error) {
    custom_alert(error);
  }
  mirror.getClients(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

//Load Get Client List -----------------------------------------------------------------------------------------
function loadClientsList(data) {
  //alert("hi");
  $('.tbody-clientunit-list').find('tr').remove();
  var sno = 0;
  var getAllArrayValues = [];

  $.each(data, function (key, value){
    var unitId = value.unit_id;
    var unitVal = 0;
    var clientId = value.client_id;
    var bgroupId = value.business_group_id;
    var lentitiesId = value.legal_entity_id;
    var divisionId = value.division_id;
    var countryId = value.country_id;
    var tableRow = $('#templates .table-clientunit-list .table-row');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.group-name', clone).text(getGroupName(clientId));
    $('.business-group-name', clone).text(getBusinessGroupName(bgroupId));
    $('.country-name', clone).text(getCountryName(countryId));
    $('.legal-entity-name', clone).text(getLegalEntityName(lentitiesId));

    //edit icon
    $('.edit').attr('title', 'Click Here to Edit');
    $('.edit', clone).addClass('fa-pencil text-primary');
    $('.edit', clone).on('click', function () {
      clientunit_edit(clientId, bgroupId, lentitiesId, countryId);
    });

    if (value.is_active == false){
      $('.status-text', clone).text("In active");
    }
    else{
      $('.status-text', clone).text("Active");
    }

    $('.tbody-clientunit-list').append(clone);
  });
}

function getGroupName(groupId) {
  var groupName;
  $.each(groupList, function (key, value) {
    if (value.client_id == groupId) {
      groupName = value.group_name;
    }
  });
  return groupName;
}
function getBusinessGroupName(businessGroupId) {
  var businessgroupName;
  $.each(businessGroupList, function (key, value) {
    if (value.business_group_id == businessGroupId) {
      businessgroupName = value.business_group_name;
    }
  });
  return businessgroupName;
}
function getLegalEntityName(legalentityId) {
  var legalEntityName;
  $.each(legalEntitiesList, function (key, value) {
    if (value.legal_entity_id == legalentityId) {
      legalEntityName = value.legal_entity_name;
    }
  });
  return legalEntityName;
}
function getCountryName(countryId) {
  var countryName;
  $.each(countryFulList, function (key, value) {
    if (value.country_id == countryId) {
      countryName = value.country_name;
    }
  });
  return countryName;
}
//Edit client Unit -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, businessgroupId, legalentityId, countryId) {
  //alert("edit")
  isUpdate = true;
  units_count = [];
  division_cnt = 0;
  $('#clientunit-view').hide();
  $('#clientunit-add').show();
  $('#group-select').hide();
  $('.labelgroup').show();
  $('#businessgroup-select').hide();
  $('.labelbusinessgroup').show();
  $('#entity-select').hide();
  $('.labelentity').show();
  $('#ac-country').hide();
  $('#country-name').hide();
  $('.labelcountry').show();

  //$('#division-text').show();
  $('#division-select').hide();
  $('#division-new').hide();
  $('#division-existing').hide();
  $('.no-of-units').val('');

  var x = document.getElementsByTagName('input');
  for (i = 0; i <= x.length - 1; i++) {
    if (x.item(i).type != 'submit') {
      x.item(i).value = '';
    }
  }
  $('#group-select').find('option').not(':first').remove();
  $('#businessgroup-select').find('option').not(':first').remove();
  $('#entity-select').find('option').not(':first').remove();
  checkunitscount = null;
  clearMessage();
  function onSuccess(data) {
    clientdomainList = data.client_domains;
    loadFormListUpdate(clientunitId, businessgroupId, legalentityId, countryId);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getClients(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
//Update load form cal------------------------------------------------------------------------------------------
function loadFormListUpdate(clientunitId, businessgroupId, legalEntityId, countryId) {
  //alert("row form")
  $('#businessgroup-update-id').val('');
  $('#legalentity-update-id').val('');
  $('#client-unit-id').val(clientunitId);
  $('.add-country-unit-list').empty();
  //group
  loadClientGroups(groupList);
  $('.labelgroup').text(getGroupName(clientunitId));

  //businessgroup
  if (businessgroupId != '') {
    loadBusinessGroups(clientunitId);
    $('#businessgroup-update-id').val(businessgroupId);
    $(".labelbusinessgroup").text(getBusinessGroupName(businessgroupId));
    //$('#businessgroup-select option[value = '+businessgroupId+']').attr('selected','selected');
  }

  if(businessgroupId == '')
  {
    $(".labelbusinessgroup").text(" --- ")
  }

  //legalentity
  loadLegalEntity(clientunitId, businessgroupId);
  $('#legalentity-update-id').val(legalEntityId);
  $(".labelentity").text(getLegalEntityName(legalEntityId));
  //$('#entity-text').val(getLegalEntityName(legalEntityId));
  //$('#entity-select option[value = '+legalEntityId+']').attr('selected','selected');

  //country
  if(countryId != '')
  LoadCountry(countryId);

  //load doamin, orgainsiation in array
  load_domain_org();

  //Load Units under division/category
  unitcount = 1;
  unit_start_cnt = 1;
  div_catg_cnt = 1;
  div_start_cnt = 2;
  divisionId = 0;
  categoryName = '';
  $.each(unitList, function (unitkey, unitval) {
    console.log("inside units")
    console.log(unitkey)
    console.log(unitval)
    unitval = unitList[unitkey];
    console.log(unitval)
    console.log("unit val div id:"+unitval.division_id)
    console.log("unit val div id:"+unitval.category_name)
    if(unitval.client_id == clientunitId && unitval.country_id == countryId && unitval.legal_entity_id == legalEntityId)
    {
      var tab_len = $('.add-country-unit-list').find('table').length;
      if(tab_len == 0 || tab_len < 0)
      {
        division_cnt = 0;
        addcountryrownew();
        loadUnitValues(unitval);
      }
      else
      {
        var rowcnt=0;
        for(var i=0;i<tab_len;i++)
        {
          var division_name;
          if(unitval.division_id != '')
          {
            division_name = getDivisionName(unitval.division_id);
          }

          if(division_name != "")
          {
            if(category_name != "")
            {
              if($('.labeldivision-'+parseInt(i+1)+'-1').text() == division_name &&
                $('.labelcategory-'+parseInt(i+1)+'-1').text() == category_name)
              {
                addNewUnitRow('btable table-'+parseInt(i+1));
                loadUnitValues(unitval);
              }
            }
            else if(category_name == "")
            {
              if($('.labeldivision-'+parseInt(i+1)+'-1').text() == division_name &&
                $('.labelcategory-'+parseInt(i+1)+'-1').text() == "--")
              {
                addNewUnitRow('btable table-'+parseInt(i+1));
                loadUnitValues(unitval);
              }
            }
          }
          else if(division_name == "")
          {
            if(category_name != "")
            {
              if($('.labeldivision-'+parseInt(i+1)+'-1').text() == "--" &&
                $('.labelcategory-'+parseInt(i+1)+'-1').text() == category_name)
              {
                addNewUnitRow('btable table-'+parseInt(i+1));
                loadUnitValues(unitval);
              }
            }
            else
            {
             if($('.labeldivision-'+parseInt(i+1)+'-1').text() == "--" &&
                $('.labelcategory-'+parseInt(i+1)+'-1').text() == "--")
              {
                addNewUnitRow('btable table-'+parseInt(i+1));
                loadUnitValues(unitval);
              }
            }
          }
          else
          {
            rowcnt = 1;
          }
        }
        if(rowcnt == 1)
        {
          rowcnt = 0;
          addcountryrownew();
          loadUnitValues(unitval);
        }
      }
    }
  });
}
// log edited domain id and organisation id
function load_domain_org()
{
  units_count = [];
  domain_ids = [];
  org_ids = [];
  for(var i=0;i<unitList.length;i++)
  {
    d_ids = unitList[i].domain_ids;
    if(d_ids.length > 0)
    {
      for(var j=0;j<d_ids.length;j++)
      {
       domain_ids.push(d_ids[j])
      }
    }
    i_ids = unitList[i].i_ids;
    if(i_ids.length > 0)
    {
      for(var j=0;j<i_ids.length;j++)
      {
       org_ids.push(i_ids[j])
      }
    }
  }


  for(var i=0;i<domain_ids.length;i++)
  {
    console.log("d:"+domain_ids[i])
    if(i==0)
      //push 0 index of domain id and org id
      units_count.push(domain_ids[i]+'-'+org_ids[i]+'-'+1);
      console.log("zero unit count:"+units_count)

    match_count = false;
    for(var j=i+1;j<=domain_ids.length;++j)
    {
      if(domain_ids[j] == domain_ids[i] && org_ids[j] == org_ids[i])
      {
        var unit_count_val = units_count[i].split("-")[2];
        units_count[i] = domain_ids[i]+'-'+org_ids[i]+'-'+ (parseInt(unit_count_val)+1);
        match_count = true;
      }
    }
    if(match_count == false)
    {
      units_count[i] = domain_ids[i]+'-'+org_ids[i]+'-'+ 1;
    }
    console.log("edit unit count:"+units_count)
  }
}
function getDivisionName(divisionId)
{
  var division_name;
  for(var i=0;i<divisionList.length;i++)
  {
    if(divisionList[i].division_id == divisionId)
    {
      division_name = divisionList[i].division_name;
      break;
    }
  }
  return division_name;
}
function loadUnitValues(unitval)
{
  //alert("inside loading")
  
  var unit_second_cnt = $('.unitcnt-'+ division_cnt + '-' + 1).val();
  var firstlist = unitval
  var cid = firstlist.country_id;
  //alert("country-id:"+cid);
  //load division
  $('.division-id-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.labeldivision-'+division_cnt+'-'+unit_second_cnt).show();
  if(firstlist.division_id != null)
  {
    $('.divisionid-'+division_cnt + '-' + unit_second_cnt).val(firstlist.division_id);
    loadDivision('division-id-' + division_cnt + '-' + unit_second_cnt);
    $('.division-id-' + division_cnt + '-' + unit_second_cnt + ' option[value=' + firstlist.division_id + ']').
      attr('selected', 'selected');
    division_name = getDivisionName(firstlist.division_id);
    $('.labeldivision-'+division_cnt+'-'+unit_second_cnt).text(division_name);
  }
  else
  {
    $('.labeldivision-'+division_cnt+'-'+unit_second_cnt).text("--");
  }

  if(firstlist.category_name != '')
  {
    $('.categoryid-'+division_cnt+'-'+unit_second_cnt).val(firstlist.category_id);
    console.log("load catg:"+$('.categoryid-'+division_cnt+'-'+unit_second_cnt).val())
    $('.category-name-'+division_cnt+'-'+unit_second_cnt).val(firstlist.category_name);
    $('.category-name-'+division_cnt+'-'+unit_second_cnt).hide();
    $('.labelcategory-'+division_cnt+'-'+unit_second_cnt).text(firstlist.category_name);
  }

  else
  {
    $('.category-name-'+division_cnt+'-'+unit_second_cnt).val();
    $('.category-name-'+division_cnt+'-'+unit_second_cnt).hide();
    $('.labelcategory-'+division_cnt+'-'+unit_second_cnt).text("--");
  }

  var gid = firstlist.geography_id;
  var unitlts = loadupdateunitlocation(gid);
  loadglevels('glevel-' + division_cnt + '-' + unit_second_cnt);
  console.log("level id:"+unitlts.level_id)
  console.log($('.glevel-' + division_cnt + '-' + unit_second_cnt));
  //loadIndustry('industry-'+countryByCount+'-'+1);
  $('.glevel-' + division_cnt + '-' + unit_second_cnt + ' option[value=' + unitlts.level_id + ']').
  attr('selected', 'selected');

  $('.glevel-' + division_cnt + '-' + unit_second_cnt).hide();
  for(var i=0;i<geographyLevelList.length;i++)
  {
    if(geographyLevelList[i].l_id == unitlts.level_id)
    {
      $('.labelgeolevels-' + division_cnt + '-' + unit_second_cnt).show();
      $('.labelgeolevels-' + division_cnt + '-' + unit_second_cnt).text(geographyLevelList[i].l_name);
    }
  }

  $('.unitlocation-' + division_cnt + '-' + unit_second_cnt).val(unitlts.gname);
  $('.unitlocation-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.unitlocation-ids-' + division_cnt + '-' + unit_second_cnt).val(gid);
  $('.unitlocation-ids-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.full-location-list-' + division_cnt + '-' + unit_second_cnt).text(unitlts.mapping);
  $('.full-location-list-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.labelunitlocation-' + division_cnt + '-' + unit_second_cnt).show();
  $('.labelunitlocation-' + division_cnt + '-' + unit_second_cnt).text(unitlts.gname);

  $('.unit-id-' + division_cnt + '-'+unit_second_cnt).val(firstlist.unit_id);

  $('.unit-code-' + division_cnt + '-' + unit_second_cnt).val(firstlist.unit_code);
  $('.unit-code-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.labelunitcode-' + division_cnt + '-' + unit_second_cnt).show();
  $('.labelunitcode-' + division_cnt + '-' + unit_second_cnt).text(firstlist.unit_code);

  $('.unit-name-' + division_cnt + '-'+unit_second_cnt).val(firstlist.unit_name);
  $('.unit-name-' + division_cnt + '-'+unit_second_cnt).hide();
  $('.labelunitname-' + division_cnt + '-' + unit_second_cnt).show();
  $('.labelunitname-' + division_cnt + '-' + unit_second_cnt).text(firstlist.unit_name);

  $('.unit-address-' + division_cnt + '-' + unit_second_cnt).val(firstlist.address);
  $('.unit-address-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.labelunitaddress-' + division_cnt + '-' + unit_second_cnt).show();
  $('.labelunitaddress-' + division_cnt + '-' + unit_second_cnt).text(firstlist.address);

  $('.postal-code-' + division_cnt + '-' + unit_second_cnt).val(firstlist.postal_code);
  $('.postal-code-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.labelpostcode-' + division_cnt + '-' + unit_second_cnt).show();
  $('.labelpostcode-' + division_cnt + '-' + unit_second_cnt).text(firstlist.postal_code);

  var domainsListArray = firstlist.domain_ids;
  console.log("domain array:"+domainsListArray)
  $('.domain-' + division_cnt + '-' + unit_second_cnt).val(domainsListArray);
  $('.domainselected-' + division_cnt + '-' + unit_second_cnt).val(domainsListArray.length + ' Selected');
  loaddomain('domain-' + division_cnt + '-' + unit_second_cnt);
  $('.domainselected-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.domain-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.ul-domain-list-' + division_cnt + '-' + unit_second_cnt).hide();
  domain_names = getDomainsName(domainsListArray);
  $('.labeldomain-' + division_cnt + '-' + unit_second_cnt).show();
  $('.labeldomain-' + division_cnt + '-' + unit_second_cnt).text(domain_names);

  var orgtypeArray = firstlist.i_ids;
  $('.orgtype-' + division_cnt + '-' + unit_second_cnt).val(orgtypeArray);
  //alert("org:"+$('.orgtype-' + division_cnt + '-' + unit_second_cnt).val());
  $('.orgtypeselected-' + division_cnt + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');
  industrytype('industry-' + division_cnt + '-' + unit_second_cnt);
  $('.orgtypeselected-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.orgtype-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.ul-orgtype-list-' + division_cnt + '-' + unit_second_cnt).hide();
  orgn_names = getOrganizationName(orgtypeArray);
  $('.labelorganization-' + division_cnt + '-' + unit_second_cnt).show();
  $('.labelorganization-' + division_cnt + '-' + unit_second_cnt).text(orgn_names);

  if (firstlist.is_active == true) {
    $('.activedclass-' + division_cnt + '-' + unit_second_cnt).text('Active');
    if($('.active_cnt-'+division_cnt+ '-' + unit_second_cnt).text() == "")
    {
      act_cnt = 1;
      $('.active_cnt-'+division_cnt+ '-' + unit_second_cnt).text("Active Unit(s):"+act_cnt);
    }
    else
    {
      act_cnt = $('.active_cnt-'+division_cnt+ '-' + unit_second_cnt).text().split(":")[1];
      $('.active_cnt-'+division_cnt+ '-' + unit_second_cnt).text("Active Unit(s):"+parseInt(act_cnt)+1);
    }
  } else {
    var classname = 'imgactivedclass-' + division_cnt + '-' + unit_second_cnt;
    // $('.activedclass-' + division_cnt + '-' + unit_second_cnt).html('<img src="/images/icon-inactive.png" onclick="reactiviteunit(this, \'' + firstlist.unit_id + '\', \'' + clientunitId + '\');">');
  }
  //alert("approve:"+firstlist.is_approved)

  if (firstlist.is_approved == "1") {
    $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Pending');
  }
  else if (firstlist.is_approved == "2") {
    $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Approved');
  }
  else if (firstlist.is_approved == "0") {
    $('.rejected-icon-' + division_cnt + '-' + unit_second_cnt).show();
    $('.rejected-icon-' + division_cnt + '-' + unit_second_cnt).attr('title',firstlist.remarks);
    $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Rejected');
    rowIndx = unit_second_cnt - 1;
    //alert("row:"+$('.tbody-unit-'+division_cnt+' tr').eq(rowIndx).text());
    $('.tbody-unit-'+division_cnt+' tr').eq(rowIndx).css("color", "rgb(255,0,0)");
  }
  $('.edit-icon-' + division_cnt + '-' + unit_second_cnt).show();
  $('.delete-icon-' + division_cnt + '-' + unit_second_cnt).hide();
  $('.active_cnt-'+division_cnt+ '-' + unit_second_cnt).show();

}
//Add Button-------------------------------------------------------------------------------------------------
$('#btn-clientunit-add').click(function () {
  isUpdate = false;
  units_count = [];
  division_cnt = 0;
  clientUnitAdd.show();
  clientUnitView.hide();
  clientSelect.show();
  bgrpSelect.show();
  leSelect.show();
  $('#ac-country').show();
  $('#country-name').show();
  $('#division-select').show();
  $('#division-new').show();
  $('#division-existing').show();
  $('.division-id').show();
  $('.labeldivision').hide();

  groupSelect_option_no.attr('disabled', false);
  busgrpSelect_option_no.attr('disabled', false);
  entitySelect_option_no.attr('disabled', false);
  $('.labelgroup').hide();
  $('.labelbusinessgroup').hide();
  $('.labelentity').hide();
  $('.labelcountry').hide();

  unitErrMsg.val('');
  checkunitscount = null;
  countryByCount = 1;
  countc = 0;
  usercountrycount = 0;
  clearMessage();
  var x = document.getElementsByTagName('input');
  for (i = 0; i <= x.length - 1; i++) {
    if (x.item(i).type != 'submit') {
      x.item(i).value = '';
    }
  }
  var y = document.getElementsByTagName('select');
  for (i = 0; i <= y.length - 1; i++) {
    y.item(i).value = '';
  }
  clientSelect.find('option').not(':first').remove();
  bgrpSelect.find('option').not(':first').remove();
  leSelect.find('option').not(':first').remove();

  countryUnitList.empty();
  loadClientGroups(groupList);
});
//Cancel Button ----------------------------------------------------------------------------------------------
$('#btn-clientunit-cancel').click(function () {
  var msgstatus = message.cancel_operation;
  $('.warning-confirm').dialog({
    title: 'Cancel',
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        clientUnitAdd.hide();
        clientUnitView.show();
        isUpdate = false;
        countryByCount = 1;
        countc = 0;
        usercountrycount = 0;
        groupSelect_option_0.empty();
        busgrpSelect_option_0.empty();
        entitySelect_option_0.empty();
      },
      Cancel: function () {
        $(this).dialog('close');
      }
    },
    open: function () {
      $('.warning-message').html(msgstatus);
    }
  });
});
//Load All Groups---------------------------------------------------------------------------------------------
function loadClientGroups(groupsList) {
  $('#group-select').focus();
  var clients = groupsList;

  for(var i =  0; i < clients.length; i++)
  {
    var obj = $(".client-drop-down option");
    var clone = obj.clone();
    clone.attr("value", clients[i].client_id);
    clone.text(clients[i].group_name);
    clientSelect.append(clone);
  }
}

//Load Business Groups  ---------------------------------------------------------------------------------------------
function loadBusinessGroups() {
  var groupId = clientSelect.val();
  busgrpSelect_option_0.remove();
  for (var i in businessGroupList) {
    if (businessGroupList[i].client_id == groupId) {
      var bgroupId = businessGroupList[i].business_group_id;
      var bgroupName = businessGroupList[i].business_group_name;
      var obj = $(".bgrp-drop-down option");
      var clone = obj.clone();
      clone.attr("value", bgroupId);
      clone.text(bgroupName);
      $('#businessgroup-select').append(clone);
    }
  }
}

//load country list in autocomplete text box
$('#country-name').keyup(function (e) {
  var textval = $(this).val();
  //alert(textval);
  loadauto_countrytext(e, textval, function (val) {
    onCountrySuccess(val);
  });
});

//store the selected country name and id
function onCountrySuccess(val)
{
  ctrySelect_name.val(val[1]);
  ctrySelect_id.val(val[0]);
  ctrySelect_name.focus();
}

function onArrowKey_Client(e, ac_item, multipleselect, callback) {
  if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 13) {
    chosen = '';
  }
  if (e.keyCode == 40) {
    if (chosen === '') {
      chosen = 0;
    } else if (chosen + 1 < $('.' + ac_item + ' li').length) {
      chosen++;
    }
    $('.' + ac_item + ' li').removeClass('auto-selected');
    $('.' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
    return false;
  }
  if (e.keyCode == 38) {
    if (chosen === '') {
      chosen = 0;
    } else if (chosen > 0) {
      chosen--;
    }
    $('.' + ac_item + ' li').removeClass('auto-selected');
    $('.' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
    return false;
  }
  if (e.keyCode == 13) {
    var ac_id = $('.' + ac_item + ' li:eq(' + chosen + ')').attr('id');
    var ac_name = $('.' + ac_item + ' li:eq(' + chosen + ')').text();
    if (multipleselect == 'country') {
      console.log("ac-name:"+ac_name);
      console.log("ac-id:"+ac-id);
      $('#country_name').val(ac_name);
      $('#country_id').val(ac_id);
      $('.glevel-' + ac_id).empty();
      //$('.autocompleteview-' + ccount).css('display', 'none');
      activate_text_arrow(ac_id, ac_name, callback);
    }
    else {
      $('.unitlocation' + ccount).val(ac_name);
      $('.unitlocation-ids' + ccount).val(ac_id);
      for (var geography in geographyList) {
          if (geographyList[geography].geography_id == parseInt(ac_id)) {
            mappingname = geographyList[geography].mapping;
          }
      }
      $('.full-location-list' + ccount).html('<br>' + mappingname);
      $('.auto-complete-unit-location').css('display', 'none');
    }

    return false;
  }
}

function loadauto_countrytext(e, textval, callback) {
  $('#country-id').val('');
  $('#ac-country').show();
  $('#ac-country ul').empty();
  var groupId;
  var bgrpId = bgrpSelect.val();
  if ($('#client-unit-id').val() != '') {
    groupId = $('#client-unit-id').val();
  } else if ($('#client-unit-id').val() == '') {
    groupId = clientSelect.val();
  }
  if (groupId == '' || groupId == 0) {
    displayMessage(message.group_required);
  } else {
    var countries = countryFulList;
    if (textval.length > 0) {
      for(var i in countries)
      {
        if (~countries[i].country_name.toLowerCase().indexOf(textval.toLowerCase()))
        {
          if(bgrpId > 0)
          {
            if(countries[i].client_id == groupId && countries[i].business_group_id == bgrpId)
            {
              var obj = $(".country-list-drop-down li");
              console.log(obj);
              var clone = obj.clone();
              clone.attr("id", countries[i].country_id);
              clone.click(function(){
                  activate_text(this, callback);
              });
              clone.text(countries[i].country_name);
              $('#ac-country ul').append(clone);
            }
          }
          else
          {
            if(countries[i].client_id == groupId)
            {
              var obj = $(".country-list-drop-down li");
              console.log(obj);
              var clone = obj.clone();
              clone.attr("id", countries[i].country_id);
              clone.click(function(){
                  activate_text(this, callback);
              });
              clone.text(countries[i].country_name);
              $('#ac-country ul').append(clone);
            }
          }
        }
      }
    }
    else {
      $('.ac-textbox').hide();
    }
  }
  onArrowKey_Client(e, 'ac-textbox', 'country', callback);
}

//Load country for edit
function LoadCountry(country_id)
{
  for(i in countryFulList)
  {
    //alert("disp:"+countriesList[i].country_id);
    if(countryFulList[i].country_id == country_id) {
      $('#country-id').val(country_id);
      $('#country-name').val(countryFulList[i].country_name);
      $('.labelcountry').text(countryFulList[i].country_name);
      break;
    }
  }
}
//Load LegalEntities ---------------------------------------------------------------------------------------------
function loadLegalEntity() {
  var clientId = clientSelect.val();
  var businessGroupId = bgrpSelect.val();
  var countryId = ctrySelect_id;
  if (businessGroupId == 0) {
    businessGroupId = null;
  }
  if (businessGroupId != null) {
    $('#entity-select').find('option:gt(0)').remove();
    $.each(legalEntitiesList, function (key, value) {
      if (value.client_id == clientId && value.business_group_id == businessGroupId) {
        var lentityId = value.legal_entity_id;
        var lentityName = value.legal_entity_name;

        var obj = $(".le-drop-down option");
        var clone = obj.clone();
        clone.attr("value", lentityId);
        clone.text(lentityName);
        leSelect.append(clone);
      }
    });
  }
  if (businessGroupId == null) {
    $('#entity-select').find('option:gt(0)').remove();
    //$('#division-select').find('option:gt(0)').remove();
    $.each(legalEntitiesList, function (key, value) {
      if (value.client_id == clientId) {
        var lentityId = value.legal_entity_id;
        var lentityName = value.legal_entity_name;
        var obj = $(".le-drop-down option");
        var clone = obj.clone();
        clone.attr("value", lentityId);
        clone.text(lentityName);
        leSelect.append(clone);
      }
    });
  }
}

function addcountryrow() {
  clearMessage();
  var groupId = clientSelect.val();
  var businessgroupid = bgrpSelect.val();
  var lentityId = leSelect.val();
  $('.add-country-unit-list').show();
  addcountryrownew();
}

//Add Country Wise List ----------------------------------------------------------------------------------------
function addcountryrownew() {
  division_cnt++;

  unit_cnt = 0;
  var countryIds = [];
  var countryFullListIds = [];
  clearMessage();
  var divCountryAddRow = $('#templates .grid-table');
  var clone = divCountryAddRow.clone();
  $('.btable', clone).addClass('table-' + division_cnt);
  $('.countryval', clone).addClass('countryval-' + division_cnt);
  $('.country', clone).addClass('country-' + division_cnt);
  //$('.autocompleteview', clone).addClass('autocompleteview-' + division_cnt);
  //$('.ulist-text', clone).addClass('ulist-text-' + division_cnt);
  alert("division_cnt:"+division_cnt)
  $('.select_business_group', clone).addClass('select_business_group-' + division_cnt + '-' + 1);
  $('.input_business_group', clone).addClass('input_business_group-' + division_cnt + '-' + 1);
  $('.divisioncnt', clone).addClass('divisioncnt-' + division_cnt + '-' + 1);
  $('.division-id', clone).addClass('division-id-' + division_cnt + '-' + 1);
  $('.division-name', clone).addClass('division-name-' + division_cnt + '-' + 1);
  $('#division-new', clone).addClass('division-new-' + division_cnt + '-' + 1);
  $('#division-existing', clone).addClass('division-existing-' + division_cnt + '-' + 1);
  $('.divisionid', clone).addClass('divisionid-' + division_cnt + '-' + 1);
  $('.labeldivision', clone).addClass('labeldivision-' + division_cnt + '-' + 1);
  $('.active_cnt', clone).addClass('active_cnt-' + division_cnt + '-' + 1);

  $('.category-name', clone).addClass('category-name-' + division_cnt + '-' + 1);
  $('.labelcategory', clone).addClass('labelcategory-' + division_cnt + '-' + 1);
  $('.categoryid', clone).addClass('categoryid-' + division_cnt + '-' + 1);

  $('.unitcnt', clone).addClass('unitcnt-' + division_cnt + '-' + 1);
  $('.sno', clone).addClass('sno-' + division_cnt + '-' + 1);

  $('.geography-levels', clone).addClass('glevel-' + division_cnt + '-' + 1);
  $('.labelgeolevels', clone).addClass('labelgeolevels-' + division_cnt + '-' + 1)

  $('.unitlocation', clone).addClass('unitlocation-' + division_cnt + '-' + 1);
  $('.labelunitlocation', clone).addClass('labelunitlocation-' + division_cnt + '-' + 1)
  $('.unit-location-ids', clone).addClass('unitlocation-ids-' + division_cnt + '-' + 1);
  $('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-' + division_cnt + '-' + 1);
  $('.unitlocationlist-text', clone).addClass('unitlocationlist-text-' + division_cnt + '-' + 1);
  $('.full-location-list', clone).addClass('full-location-list-' + division_cnt + '-' + 1);

  $('.unit-id', clone).addClass('unit-id-' + division_cnt + '-' + 1);

  $('.unitcode-checkbox', clone).addClass('unitcode-checkbox-' + division_cnt);
  $('.unit-code', clone).addClass('unit-code-' + division_cnt + '-' + 1);
  $('.labelunitcode', clone).addClass('labelunitcode-' + division_cnt + '-' + 1)

  $('.unit-name', clone).addClass('unit-name-' + division_cnt + '-' + 1);
  $('.labelunitname', clone).addClass('labelunitname-' + division_cnt + '-' + 1)

  $('.unit-address', clone).addClass('unit-address-' + division_cnt + '-' + 1);
  $('.labelunitaddress', clone).addClass('labelunitaddress-' + division_cnt + '-' + 1)

  $('.postal-code', clone).addClass('postal-code-' + division_cnt + '-' + 1);
  $('.labelpostcode', clone).addClass('labelpostcode-' + division_cnt + '-' + 1)

  $('.domain-list', clone).addClass('domain-list-' + division_cnt + '-' + 1);
  $('.domainselected', clone).addClass('domainselected-' + division_cnt + '-' + 1);
  $('.domain', clone).addClass('domain-' + division_cnt + '-' + 1);
  $('#domains', clone).addClass('domains-' + division_cnt + '-' + 1);
  $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-' + division_cnt + '-' + 1);
  $('.ul-domain-list', clone).addClass('ul-domain-list-' + division_cnt + '-' + 1);
  $('.labeldomain', clone).addClass('labeldomain-' + division_cnt + '-' + 1)

  $('.orgtype-list', clone).addClass('orgtype-list-' + division_cnt + '-' + 1);
  $('.orgtypeselected', clone).addClass('orgtypeselected-' + division_cnt + '-' + 1);
  $('.orgtype', clone).addClass('orgtype-' + division_cnt + '-' + 1);
  $('.orgtype-selectbox-view', clone).addClass('orgtype-selectbox-view-' + division_cnt + '-' + 1);
  $('.ul-orgtype-list', clone).addClass('ul-orgtype-list-' + division_cnt + '-' + 1);
  $('.labelorganization', clone).addClass('labelorganization-' + division_cnt + '-' + 1)

  $('.add-unit-row img', clone).addClass('table-addunit-' + division_cnt);
  $('.tbody-unit-list', clone).addClass('tbody-unit-' + division_cnt);
  $('.no-of-units', clone).addClass('no-of-units-' + division_cnt);
  $('.activedclass', clone).addClass('activedclass-' + division_cnt + '-' + 1);
  $('.approveclass', clone).addClass('approveclass-' + division_cnt + '-' + 1);
  $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).attr('title', 'Edit');
  $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).on('click', function () {
    unitrow_edit(division_cnt, 1);
  });
  $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).attr('title', 'Close');
  $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).on('click', function () {
    unitrow_close(division_cnt, 1);
  });
  $('.rejected-icon', clone).addClass('rejected-icon-' + division_cnt + '-' + 1);
  $('.rejected-icon', clone).addClass('rejected-icon-' + division_cnt + '-' + 1).hide();
  if($('#client-unit-id').val() > 0)
  {
    $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).show();
    $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).hide();
  }
  else
  {
    $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).hide();
    $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).hide();
  }
  //$('#unitcount').val(1);
  //$('#countrycount').val(1);
  $('.unit-error-msg', clone).addClass('unit-error-msg-' + division_cnt);
  var tab_len = $('.add-country-unit-list').find('table:eq(0)').length;
  if(tab_len > 0)
  {
    $('.add-country-unit-list').find('table:eq(0)').before(clone);
  }
  else
  {
    $('.add-country-unit-list').append(clone);
  }
  //industrytype('industry-' + countryByCount + '-' + 1);
  $('.no-of-units-' + division_cnt).val(1);
  $('.sno-' + division_cnt + '-' + 1).text(1);
  $('.activedclass-' + division_cnt + '-' + 1).text('Active');
  $('.approveclass-' + division_cnt + '-' + 1).text('Pending');
  $('.divisioncnt-'+ division_cnt + '-' + 1).val(division_cnt);
  $('.unitcnt-'+ division_cnt + '-' + 1).val(1);
  //console.log('.unitcnt-'+ division_cnt + '-' + 1);
  //console.log($('.unitcnt-'+ division_cnt + '-' + 1).val())

  /*if (division_cnt != 1) {
    $('.unitcode-checkbox-' + division_cnt).hide();
  }*/
  if ($('.unitcode-checkbox').is(':checked')) {
    $('.unit-code-' + division_cnt + '-' + 1).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
    unitcodeautogenerateids++;
  }
  //division_cnt++;
  //unit_cnt++;
  //alert(unit_cnt);
  countc++;
  countryByCount++;
  loadDomains();


  /*$('.division-id').on('change', function () {
    $('.add-country-unit-list').empty();
    countc = null;
  });*/
  $('.unit-code', clone).on('input', function (e) {
    this.value = isCommon_Unitcode($(this));
  });
  $('.unit-name', clone).on('input', function (e) {
    this.value = isCommon($(this));
  });
  $('.unit-address', clone).on('input', function (e) {
    this.value = isCommon_Address($(this));
  });
  $('.postal-code', clone).on('input', function (e) {
    this.value = isNumbers($(this));
  });
}
//Add Unit for individual Rows---------------------------------------------------------------------------------
function log_units_count(classval)
{
  console.log("insied check units")
  console.log(classval.split("-"))
  var domain_id = $('.domain'+classval).val();
  var org_id = $('.orgtype'+classval).val();
  if(units_count.length > 0)
  {
    console.log("unit len:"+units_count.length)
    for(var i=0;i<units_count.length;i++)
    {
      var split_unit = units_count[i].split("-");
      console.log(split_unit);
      if(domain_id == split_unit[0] && org_id == split_unit[1])
      {
        var assignedUnits = getOrgCount(domain_id, org_id);
        console.log("Assigned:"+assignedUnits);
        console.log("count units:"+split_unit[2])
        if(assignedUnits <= parseInt(split_unit[2]))
        {
          console.log(classval.split("-")[3])
          //if(classval.split("-")[2] == "1")
          //{
            var msgstatus = message.unit_remove;
            $('.warning-confirm').dialog({
              title: 'Remove Unit',
              buttons: {
                Ok: function () {
                  $(this).dialog('close');
                  //var index = parseInt($('.tbody-unit-'+division_cnt+' tr').length)-1;
                  var index = parseInt(classval.split("-")[2]);
                  if(index == 1)
                  {
                    //alert("main table");
                    var rowIndx = index - 1;
                    //alert($('.tbody-unit-'+division_cnt+' tr').eq(rowIndx).text());
                    $('.tbody-unit-'+division_cnt+' tr').eq(rowIndx).remove();
                  }
                  else
                  {
                    index = parseInt(classval.split("-")[1]);
                    //alert('.tbody-unit-'+index);
                    var rowIndx = 0;
                    if (parseInt($('.tbody-unit-'+index+' tr').length) > 1)
                    {
                      rowIndx = parseInt($('.tbody-unit-'+index+' tr').length) - 1;
                    }

                    //alert($('.tbody-unit-'+index+' tr').eq(rowIndx).text());
                    $('.tbody-unit-'+index+' tr').eq(rowIndx).remove();
                  }
                },
                /*Cancel: function () {
                  $(this).dialog('close');
                  prev_org_id = org_id;
                  check_org = true;
                }*/
              },
              open: function () {
                $('.warning-message').html(msgstatus);
              }
            });
          //}
          //alert("Unit count exceeded for the selected Organization");
        }
        else if(parseInt(assignedUnits) > parseInt(split_unit[2]))
        {
          units_count[i] = domain_id+'-'+org_id+'-'+(parseInt(split_unit[2])+1);
        }
      }
    }
  }
  else
  {
    units_count.push(domain_id+'-'+org_id+'-'+1);
  }
  console.log("list:"+units_count);
}
function getOrgCount(domain_id,org_id)
{
  var entityval;
  if($('#client-unit-id').val() != '')
  {
    entityval = $('#legalentity-update-id').val();
  }
  else
  {
    entityval = leSelect.val();
  }
  for(var i in domainList)
  {
    if(domainList[i].legal_entity_id == entityval && domainList[i].domain_id == domain_id
     && domainList[i].industry_id == org_id)
    {
      return domainList[i].unit_count;
    }
  }
}
function unitrow_edit(division_cnt, unit_cnt)
{
  $('.glevel-' + division_cnt + '-' + unit_cnt).show();
  $('.labelgeolevels-' + division_cnt + '-' + unit_cnt).hide();

  $('.unitlocation-' + division_cnt + '-' + unit_cnt).show();
  $('.unitlocation-ids-' + division_cnt + '-' + unit_cnt).show();
  $('.full-location-list-' + division_cnt + '-' + unit_cnt).show();
  $('.labelunitlocation-' + division_cnt + '-' + unit_cnt).hide();

  $('.unit-code-' + division_cnt + '-' + unit_cnt).show();
  $('.labelunitcode-' + division_cnt + '-' + unit_cnt).hide();

  $('.unit-name-' + division_cnt + '-'+unit_cnt).show();
  $('.labelunitname-' + division_cnt + '-' + unit_cnt).hide();

  $('.unit-address-' + division_cnt + '-' + unit_cnt).show();
  $('.labelunitaddress-' + division_cnt + '-' + unit_cnt).hide();

  $('.postal-code-' + division_cnt + '-' + unit_cnt).show();
  $('.labelpostcode-' + division_cnt + '-' + unit_cnt).hide();

  $('.domainselected-' + division_cnt + '-' + unit_cnt).show();
  $('.domain-' + division_cnt + '-' + unit_cnt).show();
  $('.ul-domain-list-' + division_cnt + '-' + unit_cnt).show();
  $('.labeldomain-' + division_cnt + '-' + unit_cnt).hide();

  $('.orgtypeselected-' + division_cnt + '-' + unit_cnt).show();
  $('.orgtype-' + division_cnt + '-' + unit_cnt).show();
  $('.ul-orgtype-list-' + division_cnt + '-' + unit_cnt).show();
  $('.labelorganization-' + division_cnt + '-' + unit_cnt).hide();

  $('.delete-icon-' + division_cnt + '-' + unit_cnt).show();
  $('.edit-icon-' + division_cnt + '-' + unit_cnt).hide();
}
function unitrow_close(division_cnt, unit_cnt)
{
  $('.delete-icon-' + division_cnt + '-' + unit_cnt).hide();
  $('.edit-icon-' + division_cnt + '-' + unit_cnt).show();
  var unit_id = $('.unit-id-' + division_cnt + '-'+unit_cnt).val();

  for(var i in unitList)
  {
    if(unitList[i].unit_id == unit_id)
    {
      loadUnitValues(unitList[i]);
    }
  }
}
function check_previous_orgn(evt)
{
  //alert(check_org);
  /*var tableclassname = $(evt).parents('table').attr('class');
  console.log(tableclassname)
  var tableclass = tableclassname.split(' ');
  var tbodyclassname = $('.' + tableclass[1]).find('tbody:eq(1)').attr('class');
  var tbodyclasses = tbodyclassname.split(' ');*/
  //alert("class:"+tbodyclassname)
  if (check_org == true)
  {
    var unitno = $('.unitcnt-'+division_cnt+'-'+1).val();
    //alert("u:"+unitno);
    var org_id = $('.orgtype-'+division_cnt+'-'+parseInt(unitno-1)).val();
    //alert("o:"+org_id)
    if(org_id == prev_org_id)
    {
      //alert("same");
      var msgstatus = message.unit_remove;
      $('.warning-confirm').dialog({
        title: 'Remove Unit',
        buttons: {
          Ok: function () {
            $(this).dialog('close');
            var index = parseInt($('.tbody-unit-'+division_cnt+' tr').parent().index());
            $('.tbody-unit-'+division_cnt+' tr').eq(index).remove();
          },
          /*Cancel: function () {
            $(this).dialog('close');
            prev_org_id = org_id;
            check_org = true;
          }*/
        },
        open: function () {
          $('.warning-message').html(msgstatus);
        }
      });
    }
    else
    {
      check_org = false;
      addNewUnitRow(evt);
    }
  }
  else
  {
    addNewUnitRow(evt);
  }

}
function addNewUnitRow(str)
{
  var countval = division_cnt;
  console.log("div val:"+$('.divisioncnt-'+countval+'-'+ 1).val());
  var unitval = parseInt($('.unitcnt-'+countval+'-'+ 1).val()) + 1;
  $('.unitcnt-'+countval+'-'+ 1).val(unitval);
  console.log('.unitcnt-'+ countval + '-' + 1);
  console.log($('.unitcnt-'+ countval + '-' + 1).val())
  console.log("unit val:"+$('.unitcnt-'+countval+'-'+ 1).val());
  var divUnitAddRow = $('#templatesUnitRow').find('tr:eq(0)');
  var clone1 = divUnitAddRow.clone();

  $('.tbody-unit-'+countval).find('tr:eq(0)').before(clone1);
  var table_tr = $('.tbody-unit-'+countval).find('tr:eq(0)');
  /*$(this).attr({
      'class': function(_, lastClass) { return $(this).attr('class').substring(0,
        ($(this).attr('class').length - 4)) + '-'+division_cnt+'-'+unitval },
      }); */
  table_tr.find('td').find('input,select,span,div,ul').each(function() {
    $(this).attr({
      'class': function(_, lastClass) { return $(this).attr('class') +
        '-'+division_cnt+'-'+unitval },
    });
  });
  $('.edit-icon-' + division_cnt + '-' + unitval).attr('title', 'Edit');
  $('.edit-icon-' + division_cnt + '-' + unitval).on('click', function () {
    unitrow_edit(division_cnt, 1);
  });
  $('.delete-icon-' + division_cnt + '-' + unitval).attr('title', 'Close');
  $('.delete-icon-' + division_cnt + '-' + unitval).on('click', function () {
    unitrow_close(division_cnt, 1);
  });

  $('.edit-icon-' + division_cnt + '-' + unitval).hide();
  $('.delete-icon-' + division_cnt + '-' + unitval).hide();
  $('.rejected-icon-' + division_cnt + '-' + (lastClassval + 1)).hide();

  if ($('.unitcode-checkbox-'+division_cnt).is(':checked')) {
    $('.unit-code-' + division_cnt + '-' + unitval).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
    unitcodeautogenerateids++;
  }
  $('.sno-'+division_cnt+'-'+unitval).text(unitval);
  $('.activedclass-' + division_cnt + '-' + unitval).text('Active');
  $('.approveclass-' + division_cnt + '-' + unitval).text('Pending');
  //industrytype('industry-' + countval + '-' + (lastClassval + 1));
  $('.unit-code-' + division_cnt + '-' + unitval).on('input', function (e) {
    this.value = isCommon_Unitcode($(this));
  });
  $('.unit-name-' + division_cnt + '-' + unitval).on('input', function (e) {
    this.value = isCommon($(this));
  });
  $('.unit-address-' + division_cnt + '-' + unitval).on('input', function (e) {
    this.value = isCommon_Address($(this));
  });
  $('.postal-code-' + division_cnt + '-' + unitval).on('input', function (e) {
    this.value = isNumbers($(this));
  });
}
function addNewUnitRow_1(str) {
  //alert("inside unit row");
  //btable table-1
  var tableclassname = $(str).parents('table').attr('class');
  console.log(tableclassname);
  var tableclass = tableclassname.split(' ');
  var countval = tableclass[1].split('-').pop();
  //alert("countval:"+countval);
  var tbodyclassname = $('.' + tableclass[1]).find('tbody:eq(1)').attr('class');
  console.log("tbodyclassname:"+tbodyclassname);
  var tbodyclasses = tbodyclassname.split(' ');
  var lastclassname = $('.' + tbodyclasses[1]).find('tr:last .geography-levels').attr('class');
  console.log("lastclassname:"+tbodyclasses[1]);
  var lastClass = lastclassname.split(' ').pop();
  var lastClassval = parseInt(lastClass.split('-').pop());
  console.log("lastClassval:"+lastClassval);
  console.log("div val:"+$('.divisioncnt-'+countval+'-'+ 1).val());
  var unitval = parseInt($('.unitcnt-'+countval+'-'+ 1).val()) + 1;
  $('.unitcnt-'+countval+'-'+ 1).val(unitval);
  console.log('.unitcnt-'+ countval + '-' + 1);
  console.log($('.unitcnt-'+ countval + '-' + 1).val())
  console.log("unit val:"+$('.unitcnt-'+countval+'-'+ 1).val());

  var divUnitAddRow = $('#templatesUnitRow .table-UnitRow-list .table-row');
  //var divUnitAddRow = $('.'+tbodyclasses[1]).find('tr');
  var clone1 = divUnitAddRow.clone();
  $('.' + tbodyclasses[1]).find('tr:eq(0)').insertBefore(clone1);
  //var tr_len = parseInt($('.'+tbodyclasses[1]).find('tr').length)-1;
  //alert(tr_len);
  //var tableRow = $('.'+tbodyclasses[1]).find('tr:eq('+tr_len+')')
  //tableRow.insertBefore(tableRow.prev());
  $('.sno', clone1).addClass('sno-' + countval + '-' + (lastClassval + 1));
  $('.geography-levels', clone1).addClass('glevel-' + countval + '-' + (lastClassval + 1));
  $('.labelgeolevels', clone1).addClass('labelgeolevels-' + countval + '-' + (lastClassval + 1));
  $('.unit-location', clone1).addClass('unitlocation-' + countval + '-' + (lastClassval + 1));
  $('.unit-location-ids', clone1).addClass('unitlocation-ids-' + countval + '-' + (lastClassval + 1));
  $('.auto-complete-unit-location', clone1).addClass('auto-complete-unit-location-' + countval + '-' + (lastClassval + 1));
  $('.unitlocationlist-text', clone1).addClass('unitlocationlist-text-' + countval + '-' + (lastClassval + 1));
  $('.full-location-list', clone1).addClass('full-location-list-' + countval + '-' + (lastClassval + 1));
  $('.labelunitlocation', clone1).addClass('labelunitlocation-' + countval + '-' + (lastClassval + 1));

  $('.unit-id', clone1).addClass('unit-id-' + countval + '-' + (lastClassval + 1));
  $('.unit-code', clone1).addClass('unit-code-' + countval + '-' + (lastClassval + 1));
  $('.labelunitcode', clone1).addClass('labelunitcode-' + countval + '-' + (lastClassval + 1));
  $('.unit-name', clone1).addClass('unit-name-' + countval + '-' + (lastClassval + 1));
  $('.labelunitname', clone1).addClass('labelunitname-' + countval + '-' + (lastClassval + 1));
  $('.unit-address', clone1).addClass('unit-address-' + countval + '-' + (lastClassval + 1));
  $('.labelunitaddress', clone1).addClass('labelunitaddress-' + countval + '-' + (lastClassval + 1));
  $('.postal-code', clone1).addClass('postal-code-' + countval + '-' + (lastClassval + 1));
  $('.labelpostcode', clone1).addClass('labelpostcode-' + countval + '-' + (lastClassval + 1));

  $('#domains', clone).addClass('domains-' + countval + '-' + (lastClassval + 1));
  $('.domain-list', clone1).addClass('domain-list-' + countval + '-' + (lastClassval + 1));
  $('.domainselected', clone1).addClass('domainselected-' + countval + '-' + (lastClassval + 1));
  $('.domain', clone1).addClass('domain-' + countval + '-' + (lastClassval + 1));
  $('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-' + countval + '-' + (lastClassval + 1));
  $('.ul-domain-list', clone1).addClass('ul-domain-list-' + countval + '-' + (lastClassval + 1));
  $('.labeldomain', clone1).addClass('labeldomain-' + countval + '-' + (lastClassval + 1));

  $('.orgtype-list', clone1).addClass('orgtype-list-' + countval + '-' + (lastClassval + 1));
  $('.orgtypeselected', clone1).addClass('orgtypeselected-' + countval + '-' + (lastClassval + 1));
  $('.orgtype', clone1).addClass('orgtype-' + countval + '-' + (lastClassval + 1));
  $('.orgtype-selectbox-view', clone1).addClass('orgtype-selectbox-view-' + countval + '-' + (lastClassval + 1));
  $('.ul-orgtype-list', clone1).addClass('ul-orgtype-list-' + countval + '-' + (lastClassval + 1));
  $('.labelorganization', clone1).addClass('labelorganization-' + countval + '-' + (lastClassval + 1));

  $('.no-of-units-' + countval).val(parseInt($('.no-of-units-' + countval).val()) + 1);

  $('.activedclass', clone1).addClass('activedclass-' + countval + '-' + (lastClassval + 1));
  $('.approveclass', clone1).addClass('approveclass-' + countval + '-' + (lastClassval + 1));
  $('.edit-icon', clone1).addClass('edit-icon-' + division_cnt + '-' + (lastClassval + 1)).attr('title', 'Edit');
  $('.edit-icon', clone1).addClass('edit-icon-' + division_cnt + '-' + (lastClassval + 1)).on('click', function () {
    unitrow_edit(division_cnt, 1);
  });
  $('.delete-icon', clone1).addClass('delete-icon-' + division_cnt + '-' + (lastClassval + 1)).attr('title', 'Close');
  $('.delete-icon', clone1).addClass('delete-icon-' + division_cnt + '-' + (lastClassval + 1)).on('click', function () {
    unitrow_close(division_cnt, 1);
  });

  $('.edit-icon', clone1).addClass('edit-icon-' + division_cnt + '-' + (lastClassval + 1)).hide();
  $('.delete-icon', clone1).addClass('delete-icon-' + division_cnt + '-' + (lastClassval + 1)).hide();
  $('.rejected-icon', clone1).addClass('rejected-icon-' + division_cnt + '-' + (lastClassval + 1));
  $('.rejected-icon', clone1).addClass('rejected-icon-' + division_cnt + '-' + (lastClassval + 1)).hide();
  /*if(tr_len > 0)
  {
    $('.' + tbodyclasses[1]).find('tr:eq(-1)').before(clone1);
  }
  else
  {
    $('.' + tbodyclasses[1]).append(clone1);
  }*/
  if ($('.unitcode-checkbox').is(':checked')) {
    $('.unit-code-' + countval + '-' + (lastClassval + 1)).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
    unitcodeautogenerateids++;
  }
  $('.sno-' + countval + '-' + (lastClassval + 1)).text(unitval);
  $('.activedclass-' + countval + '-' + (lastClassval + 1)).text('Active');
  $('.approveclass-' + countval + '-' + (lastClassval + 1)).text('Pending');
  //industrytype('industry-' + countval + '-' + (lastClassval + 1));
  $('.unit-code', clone1).on('input', function (e) {
    this.value = isCommon_Unitcode($(this));
  });
  $('.unit-name', clone1).on('input', function (e) {
    this.value = isCommon($(this));
  });
  $('.unit-address', clone1).on('input', function (e) {
    this.value = isCommon_Address($(this));
  });
  $('.postal-code', clone1).on('input', function (e) {
    this.value = isNumbers($(this));
  });

}
function intTo5digitsString(nb) {
  if (nb > 0 && nb < 10)
    return '0000' + nb;
  else if (nb >= 10 && nb < 100)
    return '000' + nb;
  else if (nb >= 100 && nb < 1000)
    return '00' + nb;
  else if (nb >= 1000 && nb < 10000)
    return '0' + nb;
}
function autoGenerateUnitCode() {
  var client_id = $('#group-select').val();
  if (client_id == '' || client_id == null || client_id == "Select") {
    client_id = $('#client-unit-id').val();
  }
  //alert("client id:"+client_id);
  function onSuccess(data) {
    console.log("unit code:"+data.next_unit_code)
    unitcodeautogenerate(data.next_unit_code);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getNextUnitCode(parseInt(client_id), function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
function unitcodeautogenerate(auto_generate_initial_value) {
  unitcodeautogenerateids = null;
  if ($('.labelgroup').text().trim() == '') {
    console.log("auto")
    unitcodeautogenerateids = auto_generate_initial_value;
    var sno = [];
    if ($('.unitcode-checkbox').is(':checked')) {
      console.log("checked")
      var groupname = $.trim($('#group-select :Selected').text());
      console.log("grp name:"+groupname)
      var groupname = groupname.replace(' ', '');
      get2CharsofGrouplower = groupname.slice(0, 2);
      get2CharsofGroup = get2CharsofGrouplower.toUpperCase();
      console.log("slice:"+get2CharsofGroup)
      var flag = 0;
      $('.add-country-unit-list .unit-code').each(function (i) {
        if ($(this).prev('.unit-id').val() == '') {
        console.log("codes")
          $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
          unitcodeautogenerateids++;
        }
        else{
          $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
          unitcodeautogenerateids++;
        }
      });
    } else {
      $('.add-country-unit-list .unit-code').each(function (i) {
        if ($(this).prev('.unit-id').val() == '') {
          $(this).val('');  //$(this).removeAttr("readonly");
        }
      });
    }
  }
  if ($('.labelgroup').text().trim() != '') {
    // client_id = $("#client-unit-id").val();
    // $.each(groupList, function(key, value){
    //     if(value['client_id'] == client_id){
    //         auto_generate_initial_value = value["next_unit_code"];
    //     }
    // });
    unitcodeautogenerateids = auto_generate_initial_value;
    var sno = [];
    if ($('.unitcode-checkbox').is(':checked')) {
      var groupname = $.trim($('.labelgroup').text());
      var groupname = groupname.replace(' ', '');
      get2CharsofGrouplower = groupname.slice(0, 2);
      get2CharsofGroup = get2CharsofGrouplower.toUpperCase();
      var flag = 0;
      $('.add-country-unit-list .unit-code').each(function (i) {
        if ($(this).prev('.unit-id').val() == '') {
          $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
          unitcodeautogenerateids++;
        }  //$(this).attr("readonly", "readonly");
      });
    } else {
      $('.add-country-unit-list .unit-code').each(function (i) {
        if ($(this).prev('.unit-id').val() == '') {
          $(this).val('');  //$(this).removeAttr("readonly");
        }
      });
    }
  }
}

//load division
function loadDivision(classval) {
  //alert("inside division");
  //alert(division_cnt);
  var lastClass = classval.split(' ').pop();
  var clientId, businessGroupId, lentityId ;
  if($('#client-unit-id').val() != '')
  {
    clientId = $('#client-unit-id').val();
    businessGroupId = $('#businessgroup-update-id').val();
    lentityId = $('legalentity-update-id').val();
  }
  else
  {
    clientId = clientSelect.val();
    businessGroupId = bgrpSelect.val();
    lentityId = leSelect.val();
  }

  $('.'+lastClass).find('option:gt(0)').remove();
  $.each(divisionList, function (key, value) {
    if(businessGroupId > 0)
    {
      if (value.client_id == clientId &&  value.business_group_id == businessGroupId && value.legal_entity_id == lentityId) {
        var divisionId = value.division_id;
        var divisionName = value.division_name;
        var obj = $('.divi-drop-down option');
        var clone = obj.clone();
        clone.attr("value", divisionId);
        clone.text(divisionName);
        $('.'+lastClass).append(clone);
      }
    }
    else
    {
      if (value.client_id == clientId && value.legal_entity_id == lentityId) {
      var divisionId = value.division_id;
      var divisionName = value.division_name;
      var obj = $('.divi-drop-down option');
        var clone = obj.clone();
        clone.attr("value", divisionId);
        clone.text(divisionName);
        $('.'+lastClass).append(clone);
      }
    }
  });
}
function divisionExistingChecking(str) {
  //alert(evtId);

  var countval = '-' + division_cnt + '-' + 1;
  alert(str)
  alert(countval)
  if (str == 'New') {
    $('.input_business_group'+countval).show();
    $('.division-name'+countval).show();
    $('.division-id'+countval).hide();
    $('.division-new'+countval).hide();
    $('.division-existing'+countval).show();
    $('.division-name'+countval).val('');
    $('.division-id'+countval).val('');
    $('.select_business_group'+countval).hide();
  }
  if (str == 'Cancel') {
    $('.select_business_group'+countval).show();
    $('.input_business_group'+countval).hide();
    $('.division-name'+countval).hide();
    $('.division-id'+countval).show();
    $('.division-new'+countval).show();
    $('.division-existing'+countval).hide();
    $('.division-name'+countval).val('');
    $('.division-id'+countval).val('');
    $('.division-id'+countval).find('option').not(':first').remove();
    loadDivision(classval);
  }
}

//Load Geography Levels -------------------------------------------------------------------------------------------
function loadglevels(classval) {
  //input-box geography-levels glevel-1-1
  var lastClass = classval.split(' ').pop();
  var checkval = lastClass.split('-');
  var countryvalue = $('#country-name').val();
  var countryid = $('#country-id').val();
  if (countryvalue == '') {
    displayMessage(message.country_required);
  } else {
    $('.' + lastClass).empty();
    var obj = $('.glevel-drop-down option');
    var clone = obj.clone();
    clone.attr("value", 0);
    clone.text("Select");
    $('.' + lastClass).append(clone);
    $.each(geographyLevelList, function (key, value) {
      obj = $('.glevel-drop-down option');
      clone = obj.clone();
      var level_id = value.l_id;
      var level_name = value.l_name;
      if(countryid == value.c_id)
        clone.attr("value", level_id);
        clone.text(level_name);
        $('.' + lastClass).append(clone);
    });
    //$('.'+lastClass +'option:gt(0)').remove();
  }
}

//set selected autocomplte value to textbox and geographylevel list
function hideunitlocation(classname) {
  var lastClass = classname.split(' ').pop();
  $('.' + lastClass).css('display', 'none');
}
function activate_unitlocaion(element, ccount, mappingname) {
  console.log(mappingname)
  var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $('.unitlocation' + ccount).val(checkname);
  $('.unitlocation-ids' + ccount).val(checkval);
  $('.full-location-list' + ccount).html('<br>' + mappingname);
}
//autocomplete location
function loadlocation(textval, classval, e) {

  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[1] + '-' + ccount[2];
  alert(countval)
  var glevelval = $('.glevel' + countval).val();
  console.log("glevel:"+glevelval)
  $('.auto-complete-unit-location' + countval).css('display', 'block');
  var suggestions = [];
  $('.unitlocationlist-text' + countval).empty();
  if (textval.length > 0) {
      for (var glist in geographyList) {
        console.log("active:"+geographyList[glist].is_active)
        if (geographyList[glist].level_id == glevelval) {
          if (~geographyList[glist].geography_name.toLowerCase().indexOf(textval.toLowerCase())
            && geographyList[glist].is_active == 1)
          {
            var obj = $(".location-list-drop-down li");
            var clone = obj.clone();
            clone.attr("id", geographyList[glist].geography_id);
            clone.click(function(){
                activate_unitlocaion(this, countval, geographyList[glist].mapping);
            });
            clone.text(geographyList[glist].geography_name);
            $('.unitlocationlist-text' + countval).append(clone);
          }
        }
      }
    //$('.unitlocationlist-text' + countval).append(str);
    //$('.unitlocation-ids'+countval).val('');
    onArrowKey_Client(e, 'unitlocationlist-text' + countval, countval, 'unit');
  }
}
function loadupdateunitlocation(gid) {
  var units = {};
  for(var i in geographyList)
  {
    var v = geographyList[i];
    if (v.geography_id == gid)
    {
      units.gname = v.geography_name;
      units.mapping = v.mapping;
      units.level_id = v.level_id;
    }
  }

  return units;
}

function changelocation(classval) {
  var lastClass = classval.split(' ').pop();
  var checkval = lastClass.split('-');
  $('.unitlocation-' + checkval[1] + '-' + checkval[2]).val('');
  $('.unitlocation-ids-' + checkval[1] + '-' + checkval[2]).val('');
  $('.full-location-list-' + checkval[1] + '-' + checkval[2]).html('');
}

//get domain for edit section
function getDomainsName(domain_ids)
{
  domain_names = [];

  for(var i=0;i<domain_ids.length;i++)
  {
    for(var j=0;j<domainList.length;j++)
    {
      if(domain_ids[i] == domainList[j].domain_id)
      {
        domain_names.push(domainList[j].domain_name);
        break;
      }
    }
  }
  return domain_names;
}

//load domains
function loadDomains()
{
  var d_ctrl = $('.domainselected-'+division_cnt+'-'+$('.unitcnt-'+division_cnt+'-'+ 1).val());
  d_ctrl.empty();
  var getClientid;
  if (($('#client-unit-id').val() == '') || ($('#client-unit-id').val() == 0)) {
    getClientid = $('#group-select').val();
  } else {
    getClientid = $('#client-unit-id').val();
  }

  if($('#client-unit-id').val() == 0)
  {
    console.log("load")
    var domains = domainList;
    var lentityId = leSelect.val();
    $.each(domains, function (key, value) {
      if(lentityId == domains[key].legal_entity_id)
      {
        console.log("le:"+lentityId);
        var optText = '<option></option>';
        /*if($.inArray(domains[key].domain_id, editdomainval) >= 0){
          optText = '<option selected="selected"></option>';
        }*/
        d_ctrl.append($(optText).val(domains[key].domain_id).html(domains[key].domain_name));
      }
    });
    d_ctrl.multiselect('rebuild');
  }
}


//get organization for edit section
function getOrganizationName(org_ids)
{
  orgn_names = [];

  for(var i=0;i<org_ids.length;i++)
  {
    for(var j=0;j<domainList.length;j++)
    {
      if(org_ids[i] == domainList[j].industry_id)
      {
        orgn_names.push(domainList[j].industry_name);
        break;
      }
    }
  }
  return orgn_names;
}

//industry
function industrytype(classval) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[1] + '-' + ccount[2];
  $('.orgtype-selectbox-view' + countval).css('display', 'block');
  var domain_id, lentityId;
  if($('#client-unit-id').val() == '')
  {
    domain_id = $('.domain' + countval).val();
    lentityId = leSelect.val();
  }
  else
  {
    domain_id = $('.domain' + countval).val();
    lentityId = $('#legalentity-update-id').val();
  }
  var editorgtypeval = [];
  if ($('.orgtype' + countval).val() != '') {
    if($('.orgtype' + countval).val().indexOf(',')!=-1)
      editorgtypeval = $('.orgtype' + countval).val().split(',');
    else
      editorgtypeval = $('.orgtype' + countval).val();
  }
  if(lentityId > 0)
  {
    if($('#client-unit-id').val() == 0)
    {
      var domains = domainList;
      $('.ul-orgtype-list' + countval).empty();
      for(var i in domains)
      {
        if(lentityId == domains[i].legal_entity_id)
        {
          var orgtypeId = parseInt(domains[i].industry_id);
          var orgtypeName = domains[i].industry_name;
          var obj = $(".orgtype-list-drop-down li");
          var clone = obj.clone();
          clone.attr("id", orgtypeId);
          clone.click(function(){
              activate_orgtype_element(this, countval);
          });
          clone.text(orgtypeName);
          $('.ul-orgtype-list' + countval).append(clone);
        }
      }
    }
    else
    {
      var domains = domainList;
      $('.ul-orgtype-list' + countval).empty();
      for(var i in domains)
      {
        var selectorgtypestatus = '';
        for (var j = 0; j < editorgtypeval.length; j++) {
          if (editorgtypeval[j] == domains[i].industry_id) {
            selectorgtypestatus = 'checked';
          }
        }
        if(lentityId == domains[i].legal_entity_id)
        {
          var orgtypeId = parseInt(domains[i].industry_id);
          var orgtypeName = domains[i].industry_name;
          var obj = $(".orgtype-list-drop-down li");
          var clone = obj.clone();
          clone.attr("id", orgtypeId);
          if(selectorgtypestatus == 'checked')
            clone.attr("class","active_org_selectbox" + countval + " active");
          clone.click(function(){
              activate_orgtype_element(this, countval);
          });
          clone.text(orgtypeName);
          $('.ul-orgtype-list' + countval).append(clone);
        }
      }
    }
  }
  else
  {
    if(lentityId == 0 && $('#client-unit-id').val() == '')
    {
      displayMessage(message.legalentity_required);
    }
    if(domain_id == 0)
    {
      displayMessage(message.domain_required);
    }
  }
  $('.orgtypeselected' + countval).val(editorgtypeval.length + ' Selected');
}
function onArrowKeyUnit(e, ac_item, count) {
  if (e.keyCode == 13) {
    chosen_unit = '';
    $('.domain-selectbox-view').hide();
  }
  if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 32) {
    chosen_unit = '';
  }
  if (e.keyCode == 40) {
    if (chosen_unit === '') {
      chosen_unit = 0;
    } else if (chosen_unit + 1 < $('.' + ac_item + ' li').length) {
      chosen_unit++;
    }
    $('.' + ac_item + ' li').removeClass('auto-selected');
    $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('auto-selected');
    return false;
  }
  if (e.keyCode == 38) {
    if (chosen_unit === '') {
      chosen_unit = 0;
    } else if (chosen_unit > 0) {
      chosen_unit--;
    }
    $('.' + ac_item + ' li').removeClass('auto-selected');
    $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('auto-selected');
    return false;
  }
  if (e.keyCode == 32) {
    $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('auto-selected');
    var ms_id = $('.' + ac_item + ' li:eq(' + chosen_unit + ')').attr('id');
    var chkstatus = $('.' + ac_item + ' li:eq(' + chosen_unit + ')').attr('class');
    if(ac_item.indexOf('domains')!=-1)
    {
      if (chkstatus == 'active_selectbox' + count + ' active') {
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active_selectbox' + count);
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active');
      }
      else {
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active_selectbox' + count);
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active');
      }
    }
    else if(ac_item.indexOf('orgtype')!=-1)
    {
      if (chkstatus == 'active_org_selectbox' + count + ' active') {
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active_org_selectbox' + count);
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active');
      }
      else {
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active_org_selectbox' + count);
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active');
      }
    }



    if(ac_item.indexOf('domains')!=-1)
    {
        activate_domain(count);
    }
    else if(ac_item.indexOf('orgtype')!=-1)
    {
        activate_orgtype(count);
    }

    return false;
  }
}

//Submit Record -----------------------------------------------------------------------------------------

$('#btn-clientunit-submit').click(function ()
{
  //alert("division_cnt:"+division_cnt);
  clearMessage();
  var clientunitIdValue = $('#client-unit-id').val();
  var groupNameValue = $('#group-select').val();
  var businessgroupValue = $('#businessgroup-select').val();
  var businessgroupName = $('#businessgroup-select :selected').text();
  var legalEntityValue = $('#entity-select').val();
  var legalEntityName = $('#entity-select :selected').text();
  var countryValue = $('#country-name')
  //var divisiontextValue = $('#division-text').val();
  //var divisionValue = $('#division-select').val();
  //var divisionName = $('#division-select :selected').text();
  var unitCountValue = $('#unitcount').val();
  var countryVal = $('#country-id').val();
  var countryName = $('#country-name').val();
  if (clientunitIdValue == '')
  {
    if (groupNameValue.length == 0) {
      displayMessage(message.group_required);
      return false;
    }
    if (countryName.length == 0) {
      if (countryVal.length == 0) {
        displayMessage(message.country_required);
        return false;
      }
    }
    if (unitCountValue.length == 0) {
      displayMessage(message.add_one_unit);
      return false;
    }
    if (countryVal.length == 0) {
      displayMessage(message.country_required);
      return false;
    }
    function onSuccess(data) {
      $('#clientunit-add').hide();
      $('#clientunit-view').show();
      initialize();
    }
    function onFailure(error) {
      if (error == 'BusinessGroupNameAlreadyExists') {
        displayMessage(message.bgroup_exists);
      } else if (error == 'LegalEntityNameAlreadyExists') {
        displayMessage(message.lentity_exists);
      } else if (error == 'DivisionNameAlreadyExists') {
        displayMessage(message.division_exists);
      } else if (error == 'UnitCodeAlreadyExists') {
        displayMessage(message.unitcode_exists);
      } else {
        displayMessage(error);
      }
    }
    var businessGroup;
    var bgIdValue;
    var bgNameValue;
    bgIdValue = parseInt(businessgroupValue);
    if (businessgroupValue != '') {
      bgNameValue = businessgroupName;
    } else {
      bgNameValue = null;
    }
    var legalEntity;
    var leIdValue;
    var leNameValue;
    leIdValue = parseInt(legalEntityValue);
    if (legalEntityValue != '') {
      leNameValue = legalEntityName;
    } else {
      leNameValue = null;
    }

    var division;
    var divIdValue;
    var divNameValue;

    var category=null;

    var units = [];
    var division_units = [];
    var unitarr = [];
    for(var i=1; i <= division_cnt; i++)
    {
      var div_arr;
      divisionValue = $('.division-id-' + i + '-' + 1).val();
      divisiontextValue = $('.division-name-' + i + '-' + 1).val();
      if (divisiontextValue == '')
      {
        divIdValue = parseInt(divisionValue);
        divNameValue = null;
      } else {
        divIdValue = null;
        divNameValue = divisiontextValue;
      }
      unit_cnt = $('.unitcnt-'+ i + '-1').val();
      console.log('.unitcnt-'+ i + '-1')
      console.log(unit_cnt);
      if($('.category-name-' + i + '-' + 1).val()!='')
      {
        category = $('.category-name-' + i + '-' + 1).val();
      }
      else
      {
        category = null;
      }
      alert("categoryName:"+category);
      div_arr = mirror.getDivisionDict(divIdValue, divNameValue, category, i, parseInt(unit_cnt));
      division_units.push(div_arr);


      if(unit_cnt > 0)
      {
        //alert("unit count:"+unit_cnt)
        for (var j=1; j <= unit_cnt; j++)
        {
          var unit;
          unitId = null;
          unitCode = $('.unit-code-' + i + '-' + j).val();
          console.log("unitcode of row"+i+"-"+j+":"+unitCode)
          unitName = $('.unit-name-' + i + '-' + j).val().trim();
          unitAddress = $('.unit-address-' + i + '-' + j).val().trim();
          unitPostalCode = $('.postal-code-' + i + '-' + j).val().trim();
          unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
          unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();
          console.log("industry:"+$('.orgtype-' + i + '-' + j).val());
          unitIndustryId = $('.orgtype-' + i + '-' + j).val();
          console.log("domains:"+unitIndustryId);
          //unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();
          unitdomain = $('.domain-' + i + '-' + j).val();
          console.log("domains:"+unitdomain);
          if (unitLocation == '' && unitGeographyId == '' && unitCode == '' && unitName == '' && unitAddress == '' && unitPostalCode == '' && unitdomain == '' && unitIndustryId == '')
          {
            if (unitcount == 1) {
              displayMessage(message.add_one_unit);
              return;
            }
            continue;
          }
          if (unitLocation == '') {
            displayMessage(message.unitlocation_required);
            return;
          } else if (unitGeographyId == '') {
            displayMessage(message.unitlocation_invalid);
            return;
          } else if (unitCode == '') {
            displayMessage(message.unitcode_required);
            return;
          } else if (unitName == '') {
            displayMessage(message.unitname_required);
            return;
          } else if (unitIndustryId == '') {
            displayMessage(message.industryname_required);
            return;
          } else if (unitAddress == '') {
            displayMessage(message.unitaddress_required);
            return;
          } else if (unitPostalCode == '') {
            displayMessage(message.unitpostal_required);
            return;
          } else if (unitdomain == '') {
            displayMessage(message.domain_required);
            return;
          } else {
            unitarr.push(unitCode);
            var hash = [];
            for (var n = unitarr.length; n--;) {
              if (typeof hash[unitarr[n]] === 'undefined')
                hash[unitarr[n]] = [];
              hash[unitarr[n]].push(n);
            }
            var duplicates = [];
            for (var key in hash) {
              if (hash.hasOwnProperty(key) && hash[key].length > 1) {
                duplicates.push(key);
              }
            }
            if (duplicates == '') {
              //domains multi select
              var arrayDomainsVal = "";
              if(unitdomain.indexOf(',')!=-1)
              {
                arrayDomainsVal = unitdomain.split(',');
              }
              else
              {
                arrayDomainsVal = unitdomain;
              }
              var arrayDomains = [];
              for (var m = 0; m < arrayDomainsVal.length; m++) {
                arrayDomains[m] = parseInt(arrayDomainsVal[m]);
              }
              var domainsVal = arrayDomains;

              //Organization Multiselect
              var arrayOrgtypeVal = "";
              if(unitIndustryId.indexOf(',')!=-1)
              {
                arrayOrgtypeVal = unitIndustryId.split(',');
              }
              else
              {
                arrayOrgtypeVal = unitIndustryId;
              }
              var arrayOrgtype = [];
              for (var m = 0; m < arrayOrgtypeVal.length; m++) {
                arrayOrgtype[m] = parseInt(arrayOrgtypeVal[m]);
              }
              var OrgtypeVal = arrayOrgtype;


              unit = mirror.getUnitDict(null, unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), domainsVal, OrgtypeVal);
              console.log("unit dict:"+unit);
              units.push(unit);
            } else {
              displayMessage(duplicates + ' Unit Code Already Exits!!!');
              return;
            }
          }
        }
      }
      else {
        displayMessage(message.add_one_unit);
        return;
      }
    }
    //alert("units length:"+units.length);
    mirror.saveClient(parseInt(groupNameValue), parseInt(bgIdValue), leIdValue, parseInt(countryVal), division_units, units, function (error, response) {
      if (error == null) {
        alert(message.unit_save);
        units_count = [];
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  //client id null -- end
  }
  else if(clientunitIdValue != '')
  {
    clearMessage();
    function onSuccess(data) {
      $('#clientunit-add').hide();
      $('#clientunit-view').show();
      initialize();
    }
    function onFailure(error) {
      if (error == 'BusinessGroupNameAlreadyExists') {
        displayMessage(message.bgroup_exists);
      } else if (error == 'LegalEntityNameAlreadyExists') {
        displayMessage(message.lentity_exists);
      } else if (error == 'DivisionNameAlreadyExists') {
        displayMessage(message.division_exists);
      } else if (error == 'UnitCodeAlreadyExists') {
        displayMessage(message.unitcode_exists);
      } else {
        displayMessage(error);
      }
    }

    client_id = $('#client-unit-id').val();
    bgIdValue = $('#businessgroup-update-id').val();
    leIdValue = $('#legalentity-update-id').val();
    countryVal = $('#country-id').val();

    var division;
    var divIdValue;
    var divNameValue;

    var category="null";

    var units = [];
    var division_units = [];
    var unitarr = [];

    for(var i=1; i <= division_cnt; i++)
    {
      //get division ctrl value
      var divi_span_ctrl = $('.division-id-'+i+'-'+1).attr('style');
      if(divi_span_ctrl == "display: none;")
      {
        divIdValue = $('.divisionid-'+i+'-'+1).val();
        divNameValue = null;
      }
      else
      {
        divisionValue = $('.division-id-' + i + '-' + 1).val();
        divisiontextValue = $('.division-name-' + i + '-' + 1).val();
        if (divisiontextValue == '')
        {
          divIdValue = parseInt(divisionValue);
          divNameValue = null;
        } else {
          divIdValue = null;
          divNameValue = divisiontextValue;
        }
      }

      //get category values
      var catg_span_ctrl = $('.category-name-'+i+'-'+1).attr('style').split(";")[1].trim();
      //alert("category_id:"+$('#category-id-'+i+'-'+1).val());
      if(catg_span_ctrl == "display: none")
      {
        alert("category:"+$('.categoryid-'+i+'-'+1));
        category = $('.labelcategory-'+i+'-'+1).text()+"-"+$('.categoryid-'+i+'-'+1).val();

        //category = null;
      }
      else
      {
        if($('.category-name-' + i + '-' + 1).val()!='')
        {
          category = $('.category-name-' + i + '-' + 1).val();
        }
        else
        {
          category = null;
        }
      }
      unit_cnt = $('.unitcnt-'+ i + '-1').val();
      console.log('.unitcnt-'+ i + '-1')
      console.log(unit_cnt);

      div_arr = mirror.getDivisionDict(parseInt(divIdValue), divNameValue, category, i, parseInt(unit_cnt));
      division_units.push(div_arr);
      if(unit_cnt > 0)
      {
        //alert("unit count:"+unit_cnt)
        for (var j=1; j <= unit_cnt; j++)
        {
          var unit;
          //alert("enter unit:"+$('.unit-id-'+i+'-'+j).val())
          var edit_icon = $('.edit-icon-'+i+'-'+j).attr('style').split(";")[2].trim();
          //alert("edit icon:"+edit_icon)
          var unitId, unitCode, unitName, unitAddress, unitPostalCode, unitGeographyId;
          var unitLocation, unitIndustryId, unitdomain;
          if(($('.unit-id-'+i+'-'+j).val() != "" && edit_icon == "display: none"))
          {
            //alert("inside unit:"+$('.unit-id-'+i+'-'+j).val())
            unitId = $('.unit-id-'+i+'-'+j).val();

            if($('.unit-code-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitCode = $('.labelunitcode-' + i + '-' + j).text();
            }
            else
            {
              unitCode = $('.unit-code-' + i + '-' + j).val();
            }
            console.log("unitcode of row"+i+"-"+j+":"+unitCode)

            if($('.unit-name-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitName = $('.labelunitname-' + i + '-' + j).text();
            }
            else
            {
              unitName = $('.unit-name-' + i + '-' + j).val();
            }

            if($('.unit-address-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitAddress = $('.labelunitaddress-' + i + '-' + j).text();
            }
            else
            {
              unitAddress = $('.unit-address-' + i + '-' + j).val();
            }

            if($('.postal-code-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitPostalCode = $('.labelpostcode-' + i + '-' + j).text();
            }
            else
            {
              unitPostalCode = $('.postal-code-' + i + '-' + j).val();
            }

            if($('.unitlocation-ids-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
            }
            else
            {
              unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
            }
            console.log("geo id of row"+i+"-"+j+":"+unitGeographyId)
            if($('.unitlocation-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitLocation = $('.labelunitlocation-' + i + '-' + j).text();
            }
            else
            {
              unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();
            }

            if($('.orgtype-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitIndustryId = $('.labelorganization-' + i + '-' + j).text();
            }
            else
            {
              unitIndustryId = $('.orgtype-' + i + '-' + j).val().trim();
            }

            if($('.domain-' + i + '-' + j).attr('style') == "display: none;")
            {
              unitdomain = $('.labeldomain-' + i + '-' + j).text();
            }
            else
            {
              unitdomain = $('.domain-' + i + '-' + j).val().trim();
            }
          }
          else if($('.unit-id-'+i+'-'+j).val() == "")
          {
            unitId = null;
            unitCode = $('.unit-code-' + i + '-' + j).val();
            console.log("unitcode of row"+i+"-"+j+":"+unitCode)
            unitName = $('.unit-name-' + i + '-' + j).val().trim();
            unitAddress = $('.unit-address-' + i + '-' + j).val().trim();
            unitPostalCode = $('.postal-code-' + i + '-' + j).val().trim();
            unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
            unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();
            console.log("industry:"+$('.orgtype-' + i + '-' + j).val());
            unitIndustryId = $('.orgtype-' + i + '-' + j).val();
            console.log("domains:"+unitIndustryId);
            //unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();
            unitdomain = $('.domain-' + i + '-' + j).val();
            console.log("domains:"+unitdomain);
          }
          if (unitLocation == '' && unitGeographyId == '' && unitCode == '' && unitName == '' && unitAddress == '' && unitPostalCode == '' && unitdomain == '' && unitIndustryId == '')
          {
            if (unitcount == 1) {
              displayMessage(message.add_one_unit);
              return;
            }
            continue;
          }
          if (unitLocation == '') {
            displayMessage(message.unitlocation_required);
            return;
          } else if (unitGeographyId == '') {
            displayMessage(message.unitlocation_invalid);
            return;
          } else if (unitCode == '') {
            displayMessage(message.unitcode_required);
            return;
          } else if (unitName == '') {
            displayMessage(message.unitname_required);
            return;
          } else if (unitIndustryId == '') {
            displayMessage(message.industryname_required);
            return;
          } else if (unitAddress == '') {
            displayMessage(message.unitaddress_required);
            return;
          } else if (unitPostalCode == '') {
            displayMessage(message.unitpostal_required);
            return;
          } else if (unitdomain == '') {
            displayMessage(message.domain_required);
            return;
          } else {
            unitarr.push(unitCode);
            var hash = [];
            for (var n = unitarr.length; n--;) {
              if (typeof hash[unitarr[n]] === 'undefined')
                hash[unitarr[n]] = [];
              hash[unitarr[n]].push(n);
            }
            var duplicates = [];
            for (var key in hash) {
              if (hash.hasOwnProperty(key) && hash[key].length > 1) {
                duplicates.push(key);
              }
            }
            console.log("duplicates:"+duplicates)
            if (duplicates == '') {
              //domains multi select
              var arrayDomainsVal = "";
              if(unitdomain.indexOf(',')!=-1)
              {
                arrayDomainsVal = unitdomain.split(',');
              }
              else
              {
                arrayDomainsVal = unitdomain;
              }
              var arrayDomains = [];
              for (var m = 0; m < arrayDomainsVal.length; m++) {
                arrayDomains[m] = parseInt(arrayDomainsVal[m]);
              }
              var domainsVal = arrayDomains;

              //Organization Multiselect
              var arrayOrgtypeVal = "";
              if(unitIndustryId.indexOf(',')!=-1)
              {
                arrayOrgtypeVal = unitIndustryId.split(',');
              }
              else
              {
                arrayOrgtypeVal = unitIndustryId;
              }
              var arrayOrgtype = [];
              for (var m = 0; m < arrayOrgtypeVal.length; m++) {
                arrayOrgtype[m] = parseInt(arrayOrgtypeVal[m]);
              }
              var OrgtypeVal = arrayOrgtype;

              unit = mirror.getUnitDict(parseInt(unitId), unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), domainsVal, OrgtypeVal);
              console.log("unit dict:"+unit);
              units.push(unit);
            } else {
              displayMessage(duplicates + ' Unit Code Already Exits!!!');
              return;
            }
          }
        }
      }
      else {
        displayMessage(message.add_one_unit);
        return;
      }
    }
    //alert("units length:"+units.length);
    mirror.saveClient(parseInt(client_id), parseInt(bgIdValue), parseInt(leIdValue), parseInt(countryVal), division_units, units, function (error, response) {
      if (error == null) {
        alert(message.unit_save);
        units_count = [];
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }

//main loop -- end
});
function resetallfilter()
{
  //alert("inside resetallfilter")
  var obj_client = $(".client-drop-down option");
  var clone_client = obj_client.clone();
  clone_client.attr("value", 0);
  clone_client.text("Select");
  clientSelect.append(clone_client);

  busgrpSelect_option_0.remove();
  var obj_bgrp = $(".bgrp-drop-down option");
  var clone_bgrp = obj_bgrp.clone();
  clone_bgrp.attr("value", 0);
  clone_bgrp.text("Select");
  $('#businessgroup-select').append(clone_bgrp);

  var obj_le = $(".le-drop-down option");
  var clone_le = obj_le.clone();
  clone_le.attr("value", 0);
  clone_le.text("Select");
  leSelect.append(clone_le);

  var obj_divi = $(".divi-drop-down option");
  var clone_divi = obj_divi.clone();
  clone_divi.attr("value", 0);
  clone_divi.text("Select");
  $('#division-select').append(clone_divi);
}

function processSearch()
{
  c_name = FilterCountry.val().toLowerCase();
  g_name = FilterGroup.val().toLowerCase();
  bg_name = FilterBGroup.val().toLowerCase();
  le_name = FilterLE.val().toLowerCase();
  unit_status = $('.search-status-li.active').attr('value');

  searchList = []
  table = $('.tbody-clientunit-list').find('tr');
  for(var i=0;i<table.length;i++){
    data = table[i];
    unit_data = unitList[i];
    data_c_name = data.cells[3].innerHTML.toLowerCase();
    data_g_name = data.cells[1].innerHTML.toLowerCase();
    data_bg_name = data.cells[2].innerHTML.toLowerCase();
    data_le_name = data.cells[4].innerHTML.toLowerCase();
    data_is_active = unit_data.is_active;


    if (
      (~data_c_name.indexOf(c_name)) && (~data_g_name.indexOf(g_name)) &&
      (~data_bg_name.indexOf(bg_name)) && (~data_le_name.indexOf(le_name))
      )
    {
      if ((unit_status == 'all' || Boolean(parseInt(unit_status)) == data_is_active)){
        searchList.push(unit_data);
      }
    }
  }

  loadClientsList(searchList);
}

function renderControls(){
  //status of the list
  Search_status_ul.click(function (event) {
    Search_status_li.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).find('i').attr('class');
    Search_status.removeClass();
    if(currentClass != undefined){
      Search_status.addClass(currentClass);
      Search_status.text('');
    }else{
      Search_status.addClass('fa');
      Search_status.text('All');
    }
    processSearch();
  });

  //loadDomains();
}

$(function () {
  initialize();
  renderControls();
});

$('#division-text').on('input', function (e) {
  this.value = isCommon($(this));
});
clientSelect.on('change', function () {
  $('.add-country-unit-list').empty();
  countc = null;
});
bgrpSelect.on('change', function () {
  $('.add-country-unit-list').empty();
  countc = null;
});
leSelect.on('change', function () {
  $('.add-country-unit-list').empty();
  countc = null;
});
Search_status.change(function() {
    processSearch();
});
FilterBox.keyup(function() {
    processSearch();
});

