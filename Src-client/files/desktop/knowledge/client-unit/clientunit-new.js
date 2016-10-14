/**
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
function initialize() {
  function onSuccess(data) {
    $('#clientunit-add').hide();
    $('#clientunit-view').show();
    isUpdate = false;
    countryByCount = 1;
    countc = 0;
    usercountrycount = 0;
    $('#group-select  option:gt(0)').empty();
    $('#businessgroup-select  option:gt(0)').empty();
    $('#entity-select  option:gt(0)').empty();
    $('#division-select  option:gt(0)').empty();
    console.log(data);
    console.log(data.geography_levels);
    groupList = data.group_company_list;
    businessGroupList = data.business_group_list;
    legalEntitiesList = data.unit_legal_entity;
    divisionList = data.divisions;
    countryFulList = data.countries;
    geographyLevelList = data.unit_geography_level_list;
    geographyList = data.unit_geographies_list;
    industryList = data.unit_industries_list;
    domainList = data.domains;
    unitList = data.unit_list;
    clientdomainList = data.client_domains;
    loadClientsList(data);
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
function getDivisionName(divisionId) {
  var divisionName;
  $.each(divisionList, function (key, value) {
    if (value.division_id == divisionId) {
      divisionName = value.division_name;
    }
  });
  return divisionName;
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
function getIndustryName(industryId) {
  var industryName;
  $.each(industryList, function (key, value) {
    if (value.country_id == industryId) {
      industryName = value.industry_name;
    }
  });
  return industryName;
}
function getGeographyLevels(countryId, levelId) {
  var geographyLevelName;
  var geoLevelListByCountry = geographyLevelList[countryId];
  $.each(geoLevelListByCountry, function (key, value) {
    if (value.l_id == levelId) {
      geographyLevelName = value.l_name;
    }
  });
  return geographyLevelName;
}
//Load Get Client List -----------------------------------------------------------------------------------------
function loadClientsList(clientunitsList) {
  //alert("hi");
  $('.tbody-clientunit-list').find('tr').remove();
  var sno = 0;
  var getAllArrayValues = [];

  /*$.each(groupList, function(key, value) {
    max[value.client_id] = value.no_of_units;
    console.log(max[value.client_id]);
    console.log(value.no_of_units);
   });*/


  $.each(unitList, function (key, value) {
    var isActive = value.is_active;
    var unitId = value.unit_id;
    var unitVal = {};
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
    $('.legal-entity-name', clone).text(getLegalEntityName(lentitiesId));
    $('.country-name', clone).text(getCountryName(countryId));
    $('.edit-icon').attr('title', 'Edit');
    $('.edit-icon', clone).on('click', function () {
      clientunit_edit(clientId, bgroupId, lentitiesId, countryId);
    });
    /*        $('.edit', clone).html('<img src = "/images/icon-edit.png" id = "editid" onclick = "clientunit_edit('+clientId+','+bgroupId+','+lentitiesId+','+divisionId+')"/>');
*/
    // $('.is-active', clone).html('<img src = "/images/'+imageName+'" title = "'+title+'" onclick = "clientunit_active('+clientId+','+lentitiesId+', '+divisionId+', '+statusVal+')"/>');
    $('.tbody-clientunit-list').append(clone);
  });
}
//Add Button-------------------------------------------------------------------------------------------------
$('#btn-clientunit-add').click(function () {
  isUpdate = false;
  $('#clientunit-add').show();
  $('#clientunit-view').hide();
  $('#group-select').show();
  $('#businessgroup-text').hide();
  $('#businessgroup-select').show();
  $('#businessgroup-new').show();
  $('#businessgroup-existing').hide();
  $('#entity-text').hide();
  $('#entity-select').show();
  $('#entity-new').show();
  $('#entity-existing').hide();
  $('#division-text').hide();
  $('#division-select').show();
  $('#division-new').show();
  $('#division-existing').hide();
  $('.no-of-units').val('');
  $('.labelgroup').text('');
  $('.labelbusinessgroup').text('');
  $('.labelentity').text('');
  $('.labeldivision').text('');
  $('#businessgroup-update-id').val('');
  $('#legalentity-update-id').val('');
  $('#division-update-id').val('');
  $('#group-select option:not(:selected)').attr('disabled', false);
  $('#businessgroup-select option:not(:selected)').attr('disabled', false);
  $('#entity-select option:not(:selected)').attr('disabled', false);
  $('#division-select option:not(:selected)').attr('disabled', false);
  $('#client-unit-id').val('');
  $('.unit-error-msg').val('');
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
  $('#group-select').find('option').not(':first').remove();
  $('#businessgroup-select').find('option').not(':first').remove();
  $('#entity-select').find('option').not(':first').remove();
  $('#division-select').find('option').not(':first').remove();
  //$('.industry').find('option').not(':first').empty();
  $('.add-country-unit-list').empty();
  divisionExistingChecking('Cancel');
  legalEntityExistingChecking('Cancel');
  businessGroupExistingChecking('Cancel');
  //alert("add clicked");
  loadClientGroups(groupList);
  $('.no-of-units').val('');
});
//Cancel Button ----------------------------------------------------------------------------------------------
$('#btn-clientunit-cancel').click(function () {
  var msgstatus = message.cancel_operation;
  $('.warning-confirm').dialog({
    title: 'Cancel',
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        $('#clientunit-add').hide();
        $('#clientunit-view').show();
        isUpdate = false;
        countryByCount = 1;
        countc = 0;
        usercountrycount = 0;
        $('#group-select  option:gt(0)').empty();
        $('#businessgroup-select  option:gt(0)').empty();
        $('#entity-select  option:gt(0)').empty();
        $('#division-select  option:gt(0)').empty();
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
  console.log(groupsList);
  $('#group-select').find('option:gt(0)').remove();
  client_group_html = "<option value = '0'>Select</option>"
  $.each(groupsList, function (key, value) {
    var groupId = value.client_id;
    var groupName = value.group_name;
    client_group_html += "<option value = "+groupId+">"+groupName+"</option>"
  });
  $('#group-select').html(client_group_html);
}

//Load Business Groups  ---------------------------------------------------------------------------------------------
function loadBusinessGroups() {
  var groupId = $('#group-select').val();
  $('#businessgroup-select').find('option:gt(0)').remove();
  for (var i in businessGroupList) {
    if (businessGroupList[i].client_id == groupId) {
      var bgroupId = businessGroupList[i].business_group_id;
      var bgroupName = businessGroupList[i].business_group_name;
      $('#businessgroup-select').append($('<option value = "' + bgroupId + '">' + bgroupName + '</option>'));
    }
  }
  $('#entity-select').find('option:gt(0)').remove();
  $.each(legalEntitiesList, function (key, value) {
    if (value.client_id == groupId) {
      var lentityId = value.legal_entity_id;
      var lentityName = value.legal_entity_name;
      $('#entity-select').append($('<option value = "' + lentityId + '">' + lentityName + '</option>'));
    }
  });
}
//Load LegalEntities ---------------------------------------------------------------------------------------------
function loadLegalEntity() {
  var clientId = $('#group-select').val();
  var businessGroupId = $('#businessgroup-select').val();
  if (businessGroupId == '') {
    businessGroupId = null;
  }
  if (businessGroupId != null) {
    $('#entity-select').find('option:gt(0)').remove();
    $('#division-select').find('option:gt(0)').remove();
    $.each(legalEntitiesList, function (key, value) {
      if (value.business_group_id == businessGroupId) {
        var lentityId = value.legal_entity_id;
        var lentityName = value.legal_entity_name;
        $('#entity-select').append($('<option value = "' + lentityId + '">' + lentityName + '</option>'));
      }
    });
  }
  if (businessGroupId == null) {
    $('#entity-select').find('option:gt(0)').remove();
    $('#division-select').find('option:gt(0)').remove();
    $.each(legalEntitiesList, function (key, value) {
      if (value.client_id == clientId && value.business_group_id == null) {
        var lentityId = value.legal_entity_id;
        var lentityName = value.legal_entity_name;
        $('#entity-select').append($('<option value = "' + lentityId + '">' + lentityName + '</option>'));
      }
    });
  }
}
//Load country
function LoadCountry(country_id)
{
  for(i in countryFulList)
  {
    //alert("disp:"+countriesList[i].country_id);
    if(countryFulList[i].country_id == country_id) {
      $('#country-id').val(country_id);
      $('#country-name').val(countryFulList[i].country_name);
      break;
    }
  }
}

//Load Divisions ---------------------------------------------------------------------------------------------
function loadDivision() {
  console.log($('#entity-select'));
  var lentityId = $('#entity-select').val();
  if(lentityId == '')
  {
      lentityId = $('#legalentity-update-id').val();
  }
  alert(lentityId)
  $('#division-select').find('option:gt(0)').remove();
  $.each(divisionList, function (key, value) {
    if (value.legal_entity_id == lentityId) {
      var divisionId = value.division_id;
      var divisionName = value.division_name;
      $('#division-select').append($('<option value = "' + divisionId + '">' + divisionName + '</option>'));
    }
  });
}
function loadIndustry(className) {
  $('.' + className).find('option:gt(0)').remove();
  $.each(industryList, function (key, value) {
    $('.' + className).append($('<option value="' + value.industry_id + '">' + value.industry_name + '</option>'));
  });
}
function loadupdateunitlocation(gid) {
  var units = {};
  $.each(geographyList, function (key, val) {
    if (val.geography_id == gid) {
      units.gname = val.geography_name;
      units.mapping = val.mapping;
      units.level_id = val.level_id;
    }
  });
  return units;
}
function checkunits(clientid, businessGroupid, legalentityid, divisionid) {
  var checkingunits = false;
  if (businessGroupid == '') {
    businessGroupid = null;
  }
  if (divisionid == '') {
    divisionid = null;
  }
  $.each(unitList, function (unitkey, unitval) {
    if (unitval.client_id == clientid && unitval.business_group_id == businessGroupid && unitval.legal_entity_id == legalentityid && unitval.division_id == divisionid) {
      var unitValues = unitval.units;
      $.each(unitValues, function (key, value) {
        var unitListVal = unitValues[key];
        var units = [];
        var j = 0;
        $.each(unitListVal, function (k, val) {
          units[j++] = val.unit_id;
        });
        addcountryrowupdate(clientid, businessGroupid, legalentityid, divisionid, key, units, countryByCount, unitval.units);
        //add country by Unit
        countryByCount++;
        checkingunits = true;
        checkunitscount = 1;
        countc++;
      });
      $('#group-select option:not(:selected)').attr('disabled', true);
      $('#businessgroup-select option:not(:selected)').attr('disabled', true);
      $('#entity-select option:not(:selected)').attr('disabled', true);
      $('#division-select option:not(:selected)').attr('disabled', true);
      $('#businessgroup-new').hide();
      $('#entity-new').hide();
      $('#division-new').hide();
    }
  });
  return checkingunits;
}
$('#group-select').on('change', function () {
  $('.add-country-unit-list').empty();
  countc = null;
});
$('#businessgroup-select').on('change', function () {
  $('.add-country-unit-list').empty();
  countc = null;
});
$('#entity-select').on('change', function () {
  $('.add-country-unit-list').empty();
  countc = null;
});
$('#division-select').on('change', function () {
  $('.add-country-unit-list').empty();
  countc = null;
});
function addcountryrow() {
  clearMessage();
  var groupId = $('#group-select').val();
  var businessgroupid = $('#businessgroup-select').val();
  var lentityId = $('#entity-select').val();
  var divisionid = $('#division-select').val();
  var businessgrouptextval = $('#businessgroup-text').val();
  var lentitytextval = $('#entity-text').val();
  var divisiontextval = $('#division-text').val();
  if (businessgrouptextval == '' && lentitytextval == '' && divisiontextval == '') {
    if (checkunitscount == null && checkunits(groupId, businessgroupid, lentityId, divisionid) == true) {
      $('#client-unit-id').val(groupId);
    } else {
      addcountryrownew();
    }
  } else {
    alert("new row");
    addcountryrownew();
  }
}
//Add Country Wise List ----------------------------------------------------------------------------------------
function addcountryrownew() {
  alert("hi");
  division_cnt++;
  if(unit_cnt > 0)
  {
    if(unit_values == '')
    {
      unit_values = unit_cnt;
    }
    else
    {
      unit_values = unit_values + "," + unit_cnt;
    }
  }
  alert(unit_values);
  unit_cnt = 0;
  var countryIds = [];
  var countryFullListIds = [];
  var groupId = $('#group-select').val();
  if (groupId == '' || groupId == null && isUpdate == true) {
    groupId = $('#client-unit-id').val();
  }
  if ($('#entity-text').val().length == 0) {
    var legalEntityValue = $('#entity-select').val();
  } else {
    var legalEntityValue = $('#entity-text').val();
  }
  var lentityId = $('#entity-select').val();
  for (var i in groupList) {
    if (groupList[i].client_id == groupId) {
      countryIds = groupList[i].country_ids;
    }
  }
  var countryArray = [];
  var countryCount = countryIds.length;
  for (var i in countryFulList) {
    countryFullListIds = countryFulList[i].country_id;
  }
  var usercountrycount = countryFulList.length;
  if (groupId == '' && isUpdate == false) {
    displayMessage(message.group_required);
  } else if (legalEntityValue == '' && isUpdate == false) {
    displayMessage(message.legalentity_new);
  }  // else if( countc >= countryCount ){
     //     displayMessage("Exceeds Maximum Number of Countries");
     // }
  else if (countc >= usercountrycount) {
    displayMessage(message.exceeds_max_countries_user);
  } else {
    clearMessage();
    if (countryCount > countc) {
      alert("countryByCount:"+countryByCount);
      var divCountryAddRow = $('#templates .grid-table').prepend("<tr></tr>");
      var clone = divCountryAddRow.clone();
      $('.btable', clone).addClass('table-' + countryByCount);
      $('.countryval', clone).addClass('countryval-' + countryByCount);
      $('.country', clone).addClass('country-' + countryByCount);
      $('.autocompleteview', clone).addClass('autocompleteview-' + countryByCount);
      $('.ulist-text', clone).addClass('ulist-text-' + countryByCount);
      $('.divisioncnt', clone).addClass('divisioncnt-' + countryByCount + '-' + 1);
      $('.division-id', clone).addClass('division-id-' + countryByCount + '-' + 1);
      $('.division-name', clone).addClass('division-name-' + countryByCount + '-' + 1);
      $('.category-name', clone).addClass('category-name-' + countryByCount + '-' + 1);
      $('.active_cnt', clone).addClass('active_cnt-' + countryByCount + '-' + 1);
      console.log("div class:"+'divisioncnt-' + countryByCount + '-' + 1);
      $('.unitcnt', clone).addClass('unitcnt-' + countryByCount + '-' + 1);
      $('.sno', clone).addClass('sno-' + countryByCount + '-' + 1);
      $('.geography-levels', clone).addClass('glevel-' + countryByCount + '-' + 1);
      $('.unit-location', clone).addClass('unitlocation-' + countryByCount + '-' + 1);
      $('.unit-location-ids', clone).addClass('unitlocation-ids-' + countryByCount + '-' + 1);
      $('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-' + countryByCount + '-' + 1);
      $('.unitlocationlist-text', clone).addClass('unitlocationlist-text-' + countryByCount + '-' + 1);
      $('.full-location-list', clone).addClass('full-location-list-' + countryByCount + '-' + 1);
      $('.unitcode-checkbox', clone).addClass('unitcode-checkbox-' + countryByCount);
      $('.unit-code', clone).addClass('unit-code-' + countryByCount);
      $('.unit-code', clone).addClass('unit-code-' + countryByCount + '-' + 1);
      $('.unit-name', clone).addClass('unit-name-' + countryByCount + '-' + 1);
      $('.unit-address', clone).addClass('unit-address-' + countryByCount + '-' + 1);
      $('.postal-code', clone).addClass('postal-code-' + countryByCount + '-' + 1);
      $('.domain-list', clone).addClass('domain-list-' + countryByCount + '-' + 1);
      $('.domainselected', clone).addClass('domainselected-' + countryByCount + '-' + 1);
      $('.domain', clone).addClass('domain-' + countryByCount + '-' + 1);
      $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-' + countryByCount + '-' + 1);
      $('.ul-domain-list', clone).addClass('ul-domain-list-' + countryByCount + '-' + 1);

      $('.orgtype-list', clone).addClass('orgtype-list-' + countryByCount + '-' + 1);
      $('.orgtypeselected', clone).addClass('orgtypeselected-' + countryByCount + '-' + 1);
      $('.orgtype', clone).addClass('orgtype-' + countryByCount + '-' + 1);
      $('.orgtype-selectbox-view', clone).addClass('orgtype-selectbox-view-' + countryByCount + '-' + 1);
      $('.ul-orgtype-list', clone).addClass('ul-orgtype-list-' + countryByCount + '-' + 1);
      $('.add-unit-row img', clone).addClass('table-addunit-' + countryByCount);
      $('.tbody-unit-list', clone).addClass('tbody-unit-' + countryByCount);
      $('.no-of-units', clone).addClass('no-of-units-' + countryByCount);
      $('.activedclass', clone).addClass('activedclass-' + countryByCount + '-' + 1);
      $('.approveclass', clone).addClass('approveclass-' + countryByCount + '-' + 1);
      $('#unitcount').val(1);
      //$('#countrycount').val(1);
      $('.unit-error-msg', clone).addClass('unit-error-msg-' + countryByCount);
      $('.add-country-unit-list').append(clone);
      //industrytype('industry-' + countryByCount + '-' + 1);
      $('.no-of-units-' + countryByCount).val(1);
      $('.sno-' + countryByCount + '-' + 1).text(1);
      $('.activedclass-' + countryByCount + '-' + 1).text('Active');
      $('.approveclass-' + countryByCount + '-' + 1).text('Pending');
      $('.divisioncnt-'+ countryByCount + '-' + 1).val(countryByCount);
      $('.unitcnt-'+ countryByCount + '-' + 1).val(1);
      if (countryByCount != 1) {
        $('.unitcode-checkbox-' + countryByCount).hide();
      }
      if ($('.unitcode-checkbox').is(':checked')) {
        $('.unit-code-' + countryByCount + '-' + 1).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
      }
      //division_cnt++;
      unit_cnt++;
      //alert(unit_cnt);
      countc++;
      countryByCount++;


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
  }
}
//Add Unit for individual Rows---------------------------------------------------------------------------------
function addNewUnitRow(str) {
  alert("inside unit row");
  //btable table-1
  var tableclassname = $(str).parents('table').attr('class');
  console.log(tableclassname);
  var tableclass = tableclassname.split(' ');
  var countval = tableclass[1].split('-').pop();

  var tbodyclassname = $('.' + tableclass[1]).find('tbody:eq(1)').attr('class');
  console.log("tbodyclassname:"+tbodyclassname);
  var tbodyclasses = tbodyclassname.split(' ');
  var lastclassname = $('.' + tbodyclasses[1]).find('tr:last .geography-levels').attr('class');
  console.log("lastclassname:"+lastclassname);
  var lastClass = lastclassname.split(' ').pop();
  var lastClassval = parseInt(lastClass.split('-').pop());
  console.log("lastClassval:"+lastClassval);
  console.log("div val:"+$('.divisioncnt-'+countval+'-'+ 1).val());
  var unitval = parseInt($('.unitcnt-'+countval+'-'+ 1).val()) + 1;
  $('.unitcnt-'+countval+'-'+ 1).val(unitval);
  console.log("unit val:"+$('.unitcnt-'+countval+'-'+ 1).val());

  var divUnitAddRow = $('#templatesUnitRow .table-UnitRow-list .table-row');
  var clone1 = divUnitAddRow.clone();
  $('.sno', clone1).addClass('sno-' + countval + '-' + (lastClassval + 1));
  $('.geography-levels', clone1).addClass('glevel-' + countval + '-' + (lastClassval + 1));
  $('.unit-location', clone1).addClass('unitlocation-' + countval + '-' + (lastClassval + 1));
  $('.unit-location-ids', clone1).addClass('unitlocation-ids-' + countval + '-' + (lastClassval + 1));
  $('.auto-complete-unit-location', clone1).addClass('auto-complete-unit-location-' + countval + '-' + (lastClassval + 1));
  $('.unitlocationlist-text', clone1).addClass('unitlocationlist-text-' + countval + '-' + (lastClassval + 1));
  $('.full-location-list', clone1).addClass('full-location-list-' + countval + '-' + (lastClassval + 1));
  $('.unit-code', clone1).addClass('unit-code-' + countval);
  $('.unit-code', clone1).addClass('unit-code-' + countval + '-' + (lastClassval + 1));
  $('.unit-name', clone1).addClass('unit-name-' + countval + '-' + (lastClassval + 1));
  //$('.industry', clone1).addClass('industry-' + countval + '-' + (lastClassval + 1));
  $('.unit-address', clone1).addClass('unit-address-' + countval + '-' + (lastClassval + 1));
  $('.postal-code', clone1).addClass('postal-code-' + countval + '-' + (lastClassval + 1));
  $('.domain-list', clone1).addClass('domain-list-' + countval + '-' + (lastClassval + 1));
  $('.domainselected', clone1).addClass('domainselected-' + countval + '-' + (lastClassval + 1));
  $('.domain', clone1).addClass('domain-' + countval + '-' + (lastClassval + 1));
  $('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-' + countval + '-' + (lastClassval + 1));
  $('.ul-domain-list', clone1).addClass('ul-domain-list-' + countval + '-' + (lastClassval + 1));
  $('.orgtype-list', clone1).addClass('orgtype-list-' + countryByCount + '-' + 1);
  $('.orgtypeselected', clone1).addClass('orgtypeselected-' + countryByCount + '-' + 1);
  $('.orgtype', clone1).addClass('orgtype-' + countryByCount + '-' + 1);
  $('.orgtype-selectbox-view', clone1).addClass('orgtype-selectbox-view-' + countryByCount + '-' + 1);
  $('.ul-orgtype-list', clone1).addClass('ul-orgtype-list-' + countryByCount + '-' + 1);
  $('.no-of-units-' + countval).val(parseInt($('.no-of-units-' + countval).val()) + 1);
  //$('#unitcount').val(lastClassval + 1);

  $('.activedclass', clone1).addClass('activedclass-' + countval + '-' + (lastClassval + 1));
  $('.approveclass', clone1).addClass('approveclass-' + countval + '-' + (lastClassval + 1));
  $('.' + tbodyclasses[1]).append(clone1);
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
  if (client_id == '' || client_id == null) {
    client_id = $('#client-unit-id').val();
  }
  function onSuccess(data) {
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
    // client_id = $("#group-select").val();
    // $.each(groupList, function(key, value){
    //     if(value['client_id'] == client_id){
    //         auto_generate_initial_value = value["next_unit_code"];
    //     }
    // });
    //auto_generate_initial_value =
    unitcodeautogenerateids = auto_generate_initial_value;
    var sno = [];
    if ($('.unitcode-checkbox').is(':checked')) {
      var groupname = $.trim($('#group-select :Selected').text());
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
function loadglevelsupdate(countryid, lastClass) {
  if (countryid == '') {
    displayMessage(message.country_required);
  } else {
    $('.' + lastClass).find('option').not(':first').remove();
    geo_level_html = "<option value = '0'>Select</option>"
    $.each(geographyLevelList, function (key, value) {
      var level_id = value.l_id;
      var level_name = value.l_name;
      if(countryid == value.c_id)
        geo_level_html += "<option value = "+level_id+">"+level_name+"</option>"
    });
      $('.' + lastClass).html(geo_level_html);
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
    $('.' + lastClass).find('option').not(':first').remove();
    geo_level_html = "<option value = '0'>Select</option>"
    $.each(geographyLevelList, function (key, value) {
      var level_id = value.l_id;
      var level_name = value.l_name;
      if(countryid == value.c_id)
        geo_level_html += "<option value = "+level_id+">"+level_name+"</option>"
    });
      $('.' + lastClass).html(geo_level_html);
    }
}


function changelocation(classval) {
  var lastClass = classval.split(' ').pop();
  var checkval = lastClass.split('-');
  $('.unitlocation-' + checkval[1] + '-' + checkval[2]).val('');
  $('.unitlocation-ids-' + checkval[1] + '-' + checkval[2]).val('');
  $('.full-location-list-' + checkval[1] + '-' + checkval[2]).html('');
}
//load industry type--------------------------------------------------------------------------------------------------
function industrytype(classval) {
  //alert($('.orgtype' + countval).val());
  console.log(classval);
  //var lastClass = classval.split(' ').pop();
  //var lastClass = classval;
  //var checkval = lastClass.split('-');industryty
  var lastClass = classval.split(' ').pop();
  console.log("lc:"+lastClass);
  var ccount = lastClass.split('-');
  console.log("cc:"+ccount);
  var countval = '-' + ccount[1] + '-' + ccount[2];
  console.log("cv:"+countval);
  console.log("country val:"+$("#country-id").val());
  console.log("domain val:"+$('.domain' + countval).val());
  $('.orgtype-selectbox-view' + countval).css('display', 'block');
  var domain_id = $('.domain' + countval).val();
  var country_id = $("#country-id").val();

  var editorgtypeval = [];
  if ($('.orgtype' + countval).val() != '') {
    alert($('.orgtype' + countval).val())
    if($('.orgtype' + countval).val().indexOf(',')!=-1)
      editorgtypeval = $('.orgtype' + countval).val().split(',');
    else
      editorgtypeval = $('.orgtype' + countval).val();
    }
  console.log("orgtype edit:"+editorgtypeval);

  if (($('#client-unit-id').val() == '') || ($('#client-unit-id').val() == 0)) {
    var orgtypes = industryList;
    console.log("length:"+orgtypes.length);
    $('.ul-orgtype-list' + countval).empty();
    var str = '';
    for (var i in orgtypes) {
      var selectorgtypestatus = '';
      if(editorgtypeval.length > 0)
      {
        for (var j = 0; j < editorgtypeval.length; j++) {
          if (editorgtypeval[j] == orgtypes[i].industry_id) {
            selectorgtypestatus = 'checked';
          }
        }
      }
      var orgtypeId = parseInt(orgtypes[i].industry_id);
      var orgtypeName = orgtypes[i].industry_name;
      if(country_id == orgtypes[i].country_id && domain_id == orgtypes[i].domain_id)
      {
          console.log("enter id:"+orgtypes[i].country_id);;
          console.log("enter domain:"+orgtypes[i].country_id);
          if (selectorgtypestatus == 'checked') {
          str += '<li id="' + orgtypeId + '" class="active_org_selectbox' + countval + ' active" onclick="activate_orgtype_element(this, \'' + countval + '\')" >' + orgtypeName + '</li> ';
        } else {
          str += '<li id="' + orgtypeId + '" onclick="activate_orgtype_element(this, \'' + countval + '\')" >' + orgtypeName + '</li> ';
        }
      }
    }
  } else if ($('#client-unit-id').val() != '') {
    $('.ul-orgtype-list' + countval).empty();
    var str = '';
    var orgtypes = industryList;
    for (var i in orgtypes) {
      var selectorgtypestatus = '';
      for (var j = 0; j < editorgtypeval.length; j++) {
        if (editorgtypeval[j] == orgtypes[i].industry_id) {
          selectorgtypestatus = 'checked';
        }
      }
      var orgtypeId = parseInt(orgtypes[i].industry_id);
      var orgtypeName = orgtypes[i].industry_name;
      if(country_id == orgtypes[i].country_id && domain_id == orgtypes[i].domain_id)
      {
          console.log("enter id:"+orgtypes[i].country_id);;
          console.log("enter domain:"+orgtypes[i].country_id);

          if (selectorgtypestatus == 'checked') {
          str += '<li id="' + orgtypeId + '" class="active_org_selectbox' + countval + ' active" onclick="activate_orgtype_element(this, \'' + countval + '\')" >' + orgtypeName + '</li> ';
        } else {
          str += '<li id="' + orgtypeId + '" onclick="activate_orgtype_element(this, \'' + countval + '\')" >' + orgtypeName + '</li> ';
        }
      }
    }
  }
  console.log("orgtype str:"+str)
  $('.ul-orgtype-list' + countval).append(str);
  $('.orgtypeselected' + countval).val(editorgtypeval.length + ' Selected');
/////////////////////////////////////////////////////
  /*$('.' + classval).find('option').not(':first').remove();
  $('.' + classval).append($('<option value = "">Select</option>'));
  for (var industry in industryList) {

    $('.' + classval).append($('<option value = "' + industryList[industry].industry_id + '">' + industryList[industry].industry_name + '</option>'));
  }*/
}
//Edit client Unit -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, businessgroupId, legalentityId, countryId) {
  alert("edit")
  isUpdate = true;
  $('#clientunit-view').hide();
  $('#clientunit-add').show();
  $('#group-select').hide();
  $('#businessgroup-text').show();
  $('#businessgroup-select').hide();
  $('#businessgroup-new').hide();
  $('#businessgroup-existing').hide();
  $('#entity-text').show();
  $('#entity-select').hide();
  $('#entity-new').hide();
  $('#entity-existing').hide();

  //$('#division-text').show();
  $('#division-select').show();
  $('#division-new').show();
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
  $('#division-select').find('option').not(':first').remove();
  //$('.industry').find('option').not(':first').remove();
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
  alert("row form")
  $('#businessgroup-update-id').val('');
  $('#legalentity-update-id').val('');
  $('#division-update-id').val('');
  countryByCount = 1;
  $('#client-unit-id').val(clientunitId);
  $('.add-country-unit-list').empty();
  //group
  loadClientGroups(groupList);
  $('.labelgroup').text(getGroupName(clientunitId));
  //$('#group-select option[value = '+clientunitId+']').attr('selected','selected');
  //businessgroup
  if (businessgroupId != '') {
    loadBusinessGroups(clientunitId);
    $('#businessgroup-update-id').val(businessgroupId);
    // $(".labelbusinessgroup").text(getBusinessGroupName(businessgroupId));
    $('#businessgroup-text').val(getBusinessGroupName(businessgroupId));  //$('#businessgroup-select option[value = '+businessgroupId+']').attr('selected','selected');
  }
  if (businessgroupId == null) {
    //$(".labelbusinessgroup").text('');
    $('#businessgroup-text').hide();  //$('#businessgroup-select').append($('<option value = "">select</option>'));
  }
  //legalentity
  loadLegalEntity(clientunitId, businessgroupId);
  $('#legalentity-update-id').val(legalEntityId);
  //$(".labelentity").text(getLegalEntityName(legalEntityId));
  $('#entity-text').val(getLegalEntityName(legalEntityId));
  //$('#entity-select option[value = '+legalEntityId+']').attr('selected','selected');

  //country
  if(countryId != '')
  LoadCountry(countryId);

  //Division
 /* if (divisionId != '') {
    loadDivision(legalEntityId);
    $('#division-update-id').val(divisionId);
    $('#division-text').val(getDivisionName(divisionId));  //$(".labeldivision").text(getDivisionName(divisionId));
                                                           //$('#division-select option[value = '+divisionId+']').attr('selected','selected');
  }
  if (divisionId == null) {
    $('#division-text').hide();  //$(".labeldivision").text('');
                                 //$('#division-select').append($('<option value = "">select</option>'));
  }*/
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
    //if no division selected for the unit
    if(unitval.division_id == null || unitval.division_id == 0 || unitval.division_id == '')
    {
      //if no category name and no division for the unit
      if(unitval.category_name == null || unitval.category_name == '')
      {
        addUnitRowUpdate(unitval, unit_start_cnt, unitcount);
        unitcount++;
      }
      else // if category name available and no division
      {
        if(unitval.category_name == categoryName)
        {
          if(div_catg_cnt == 1)
          {
            addcountryrowupdate(unitval, div_start_cnt, div_catg_cnt);
          }
          else
          {
            addUnitListRowUpdate(unitval, div_start_cnt, div_catg_cnt);
          }
          div_catg_cnt++;
          division_cnt = div_start_cnt;
        }
        else
        {
          if(div_catg_cnt == 1)
          {
            addcountryrowupdate(unitval, div_start_cnt, div_catg_cnt);
          }
          else
          {
            addUnitListRowUpdate(unitval, div_start_cnt, div_catg_cnt);
          }
          //addcountryrowupdate(unitval, div_start_cnt, div_catg_cnt);
          div_catg_cnt++;
          div_start_cnt++;
          division_cnt = div_start_cnt;
        }
      }
    }
    //if division selected for the unit
    else
    {
      //load division
      //loadDivision(legalEntityId);
      //$('division-id-' + div_start_cnt + '-' + div_catg_cnt + ' option[value=' + unitval.division_id + ']').attr('selected', 'selected');

      //if no category name and division available for the unit
      if(unitval.category_name == null || unitval.category_name == '')
      {
        if(div_catg_cnt == 1)
        {
          addcountryrowupdate(unitval, div_start_cnt, div_catg_cnt);
        }
        else
        {
          addUnitListRowUpdate(unitval, div_start_cnt, div_catg_cnt);
        }
        //addcountryrowupdate(unitval, div_start_cnt, div_catg_cnt);
        div_catg_cnt++;
      }
      else // if category name available and division available
      {
        if(div_catg_cnt == 1)
        {
          addcountryrowupdate(unitval, div_start_cnt, div_catg_cnt);
        }
        else
        {
          addUnitListRowUpdate(unitval, div_start_cnt, div_catg_cnt);
        }
        //addcountryrowupdate(unitval, div_start_cnt, div_catg_cnt);
        div_catg_cnt++;
        div_start_cnt++;
        division_cnt = div_start_cnt;
      }
    }
    divisionId = unitval.division_id;
    categoryName = unitval.category_name;
  });
}
function addUnitRowUpdate(unitval, unit_start_cnt, unit_second_cnt)
{
  alert("without division/category");
  console.log("unit start:"+unit_start_cnt);
  console.log("unit end:"+unit_second_cnt);
  var countryByCount = unit_start_cnt;
  var divCountryAddRow = $('#templates .grid-table');
  var clone3 = divCountryAddRow.clone();
  $('.btable', clone3).addClass('table-' + countryByCount);
  $('.countryval', clone3).addClass('countryval-' + countryByCount);
  $('.country', clone3).addClass('country-' + countryByCount);
  $('.autocompleteview', clone3).addClass('autocompleteview-' + countryByCount);
  $('.ulist-text', clone3).addClass('ulist-text-' + countryByCount);
  $('.divisioncnt', clone3).addClass('divisioncnt-' + countryByCount + '-' + unit_second_cnt);
  $('.division-id', clone3).addClass('division-id-' + countryByCount + '-' + unit_second_cnt);
  $('.division-name', clone3).addClass('division-name-' + countryByCount + '-' + unit_second_cnt);
  $('.category-name', clone3).addClass('category-name-' + countryByCount + '-' + unit_second_cnt);
  $('.active_cnt', clone3).addClass('active_cnt-' + countryByCount + '-' + unit_second_cnt);
  $('.unitcnt', clone3).addClass('unitcnt-' + countryByCount + '-' + unit_second_cnt);
  $('.sno', clone3).addClass('sno-' + countryByCount + '-' + unit_second_cnt);
  $('.geography-levels', clone3).addClass('glevel-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-location', clone3).addClass('unitlocation-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-location-ids', clone3).addClass('unitlocation-ids-' + countryByCount + '-' + unit_second_cnt);
  $('.auto-complete-unit-location', clone3).addClass('auto-complete-unit-location-' + countryByCount + '-' + unit_second_cnt);
  $('.unitlocationlist-text', clone3).addClass('unitlocationlist-text-' + countryByCount + '-' + unit_second_cnt);
  $('.full-location-list', clone3).addClass('full-location-list-' + countryByCount + '-' + unit_second_cnt);
  $('.unitcode-checkbox', clone3).addClass('unitcode-checkbox-' + countryByCount);
  $('.unit-code', clone3).addClass('unit-code-' + countryByCount);
  $('.unit-code', clone3).addClass('unit-code-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-name', clone3).addClass('unit-name-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-address', clone3).addClass('unit-address-' + countryByCount + '-' + unit_second_cnt);
  $('.postal-code', clone3).addClass('postal-code-' + countryByCount + '-' + unit_second_cnt);
  $('.domain-list', clone3).addClass('domain-list-' + countryByCount + '-' + unit_second_cnt);
  $('.domainselected', clone3).addClass('domainselected-' + countryByCount + '-' + unit_second_cnt);
  $('.domain', clone3).addClass('domain-' + countryByCount + '-' + unit_second_cnt);
  $('.domain-selectbox-view', clone3).addClass('domain-selectbox-view-' + countryByCount + '-' + unit_second_cnt);
  $('.ul-domain-list', clone3).addClass('ul-domain-list-' + countryByCount + '-' + unit_second_cnt);

  $('.orgtype-list', clone3).addClass('orgtype-list-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtypeselected', clone3).addClass('orgtypeselected-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtype', clone3).addClass('orgtype-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtype-selectbox-view', clone3).addClass('orgtype-selectbox-view-' + countryByCount + '-' + unit_second_cnt);
  $('.ul-orgtype-list', clone3).addClass('ul-orgtype-list-' + countryByCount + '-' + unit_second_cnt);
  $('.add-unit-row img', clone3).addClass('table-addunit-' + countryByCount);
  $('.tbody-unit-list', clone3).addClass('tbody-unit-' + countryByCount);
  $('.no-of-units', clone3).addClass('no-of-units-' + countryByCount);
  $('.activedclass', clone3).addClass('activedclass-' + countryByCount + '-' + unit_second_cnt);
  $('.approveclass', clone3).addClass('approveclass-' + countryByCount + '-' + unit_second_cnt);
  $('#unitcount').val(unit_second_cnt);
  //$('#countrycount').val(1);
  $('.unit-error-msg', clone3).addClass('unit-error-msg-' + countryByCount);
  $('.add-country-unit-list').append(clone3);
  //industrytype('industry-' + countryByCount + '-' + 1);
  $('.no-of-units-' + countryByCount).val(countryByCount);
  $('.sno-' + countryByCount + '-' + unit_second_cnt).text(unit_second_cnt);
  $('.divisioncnt-'+ countryByCount + '-' + unit_second_cnt).val(countryByCount);
  $('.unitcnt-'+ countryByCount + '-' + unit_second_cnt).val(unit_second_cnt);
  if (countryByCount != 1) {
    $('.unitcode-checkbox-' + countryByCount).hide();
  }
  $('.unit-code', clone3).on('input', function (e) {
    this.value = isCommon_Unitcode($(this));
  });
  $('.unit-name', clone3).on('input', function (e) {
    this.value = isCommon($(this));
  });
  $('.unit-address', clone3).on('input', function (e) {
    this.value = isCommon_Address($(this));
  });
  $('.postal-code', clone3).on('input', function (e) {
    this.value = isNumbers($(this));
  });
  var firstlist = unitval
  var cid = firstlist.country_id;

  //load division
  if(firstlist.division_id != null)
  {
    loadDivision();
    $('.division-id-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + firstlist.division_id + ']').attr('selected', 'selected');
  }
  if(firstlist.category_name != '')
  {
    $('.category-name-' + unit_start_cnt + '-' + unitcount).val(unitval.category_name);
  }
  var gid = firstlist.geography_id;
  var unitlts = loadupdateunitlocation(gid);
  loadglevelsupdate(cid, 'glevel-' + countryByCount + '-' + unit_second_cnt);
  console.log("level id:"+unitlts.level_id)
  console.log($('.glevel-' + countryByCount + '-' + unit_second_cnt));
  //loadIndustry('industry-'+countryByCount+'-'+1);
  $('.glevel-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + unitlts.level_id + ']').attr('selected', 'selected');
  $('.unitlocation-' + countryByCount + '-' + unit_second_cnt).val(unitlts.gname);
  $('.unitlocation-ids-' + countryByCount + '-' + unit_second_cnt).val(gid);
  $('.full-location-list-' + countryByCount + '-' + unit_second_cnt).text(unitlts.mapping);
  $('.unit-id-' + countryByCount + '-'+unit_second_cnt).val(firstlist.unit_id);
  $('.unit-code-' + countryByCount + '-' + unit_second_cnt).val(firstlist.unit_code);
  $('.unit-name-' + countryByCount + '-'+unit_second_cnt).val(firstlist.unit_name);
  //$('.industry-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + firstlist.industry_id + ']').attr('selected', 'selected');
  $('.unit-address-' + countryByCount + '-' + unit_second_cnt).val(firstlist.unit_address);
  $('.postal-code-' + countryByCount + '-' + unit_second_cnt).val(firstlist.postal_code);
  var domainsListArray = firstlist.domain_ids;
  $('.domain-' + countryByCount + '-' + unit_second_cnt).val(domainsListArray);
  $('.domainselected-' + countryByCount + '-' + unit_second_cnt).val(domainsListArray.length + ' Selected');
  loaddomain('domain-' + countryByCount + '-' + unit_second_cnt);

  var orgtypeArray = firstlist.i_ids;
  $('.orgtype-' + countryByCount + '-' + unit_second_cnt).val(orgtypeArray);
  alert("org:"+$('.orgtype-' + countryByCount + '-' + unit_second_cnt).val());
  $('.orgtypeselected-' + countryByCount + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');
  industrytype('industry-' + countryByCount + '-' + unit_second_cnt);
  if (firstlist.is_active == true) {
    $('.activedclass-' + countryByCount + '-' + unit_second_cnt).text('Active');
  } else {
    var classnamec = 'imgactivedclass-' + countryByCount + '-' + unit_second_cnt;
    $('.activedclass-' + countryByCount + '-' + unit_second_cnt).html('<img src="/images/icon-inactive.png" onclick="reactiviteunit(this, \'' + firstlist.unit_id + '\', \'' + clientunitId + '\');">');
  }
  if (firstlist.approve_status == "1") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Pending');
  }
  else if (firstlist.approve_status == "2") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Approved');
  }
  else if (firstlist.approve_status == "0") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Rejected');
  }
}

function addUnitListRowUpdate(unitval, unit_start_cnt, unit_second_cnt)
{
  alert("without division/category");
  console.log("unit start:"+unit_start_cnt);
  console.log("unit end:"+unit_second_cnt);
  var countryByCount = unit_start_cnt;
  var divUnitListAddRow = $('#templatesUnitRow .table-UnitRow-list .table-row');
  var clone2 = divUnitAddRow.clone();
  $('.btable', clone2).addClass('table-' + countryByCount);
  $('.countryval', clone2).addClass('countryval-' + countryByCount);
  $('.country', clone2).addClass('country-' + countryByCount);
  $('.autocompleteview', clone2).addClass('autocompleteview-' + countryByCount);
  $('.ulist-text', clone2).addClass('ulist-text-' + countryByCount);
  $('.divisioncnt', clone2).addClass('divisioncnt-' + countryByCount + '-' + unit_second_cnt);
  $('.division-id', clone2).addClass('division-id-' + countryByCount + '-' + unit_second_cnt);
  $('.division-name', clone2).addClass('division-name-' + countryByCount + '-' + unit_second_cnt);
  $('.category-name', clone2).addClass('category-name-' + countryByCount + '-' + unit_second_cnt);
  $('.active_cnt', clone2).addClass('active_cnt-' + countryByCount + '-' + unit_second_cnt);
  $('.unitcnt', clone2).addClass('unitcnt-' + countryByCount + '-' + unit_second_cnt);
  $('.sno', clone2).addClass('sno-' + countryByCount + '-' + unit_second_cnt);
  $('.geography-levels', clone2).addClass('glevel-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-location', clone2).addClass('unitlocation-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-location-ids', clone2).addClass('unitlocation-ids-' + countryByCount + '-' + unit_second_cnt);
  $('.auto-complete-unit-location', clone2).addClass('auto-complete-unit-location-' + countryByCount + '-' + unit_second_cnt);
  $('.unitlocationlist-text', clone2).addClass('unitlocationlist-text-' + countryByCount + '-' + unit_second_cnt);
  $('.full-location-list', clone2).addClass('full-location-list-' + countryByCount + '-' + unit_second_cnt);
  $('.unitcode-checkbox', clone).addClass('unitcode-checkbox-' + countryByCount);
  $('.unit-code', clone2).addClass('unit-code-' + countryByCount);
  $('.unit-code', clone2).addClass('unit-code-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-name', clone2).addClass('unit-name-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-address', clone2).addClass('unit-address-' + countryByCount + '-' + unit_second_cnt);
  $('.postal-code', clone2).addClass('postal-code-' + countryByCount + '-' + unit_second_cnt);
  $('.domain-list', clone2).addClass('domain-list-' + countryByCount + '-' + unit_second_cnt);
  $('.domainselected', clone2).addClass('domainselected-' + countryByCount + '-' + unit_second_cnt);
  $('.domain', clone2).addClass('domain-' + countryByCount + '-' + unit_second_cnt);
  $('.domain-selectbox-view', clone2).addClass('domain-selectbox-view-' + countryByCount + '-' + unit_second_cnt);
  $('.ul-domain-list', clone2).addClass('ul-domain-list-' + countryByCount + '-' + unit_second_cnt);

  $('.orgtype-list', clone2).addClass('orgtype-list-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtypeselected', clone2).addClass('orgtypeselected-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtype', clone2).addClass('orgtype-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtype-selectbox-view', clone2).addClass('orgtype-selectbox-view-' + countryByCount + '-' + unit_second_cnt);
  $('.ul-orgtype-list', clone2).addClass('ul-orgtype-list-' + countryByCount + '-' + unit_second_cnt);
  $('.add-unit-row img', clone2).addClass('table-addunit-' + countryByCount);
  $('.tbody-unit-list', clone2).addClass('tbody-unit-' + countryByCount);
  $('.no-of-units', clone2).addClass('no-of-units-' + countryByCount);
  $('.activedclass', clone2).addClass('activedclass-' + countryByCount + '-' + unit_second_cnt);
  $('.approveclass', clone2).addClass('approveclass-' + countryByCount + '-' + unit_second_cnt);
  $('#unitcount').val(unit_second_cnt);
  //$('#countrycount').val(1);
  $('.unit-error-msg', clone2).addClass('unit-error-msg-' + countryByCount);
  $('.add-country-unit-list').append(clone2);
  //industrytype('industry-' + countryByCount + '-' + 1);
  $('.no-of-units-' + countryByCount).val(countryByCount);
  $('.sno-' + countryByCount + '-' + unit_second_cnt).text(unit_second_cnt);
  $('.divisioncnt-'+ countryByCount + '-' + unit_second_cnt).val(countryByCount);
  $('.unitcnt-'+ countryByCount + '-' + unit_second_cnt).val(unit_second_cnt);
  if (countryByCount != 1) {
    $('.unitcode-checkbox-' + countryByCount).hide();
  }
  $('.unit-code', clone2).on('input', function (e) {
    this.value = isCommon_Unitcode($(this));
  });
  $('.unit-name', clone2).on('input', function (e) {
    this.value = isCommon($(this));
  });
  $('.unit-address', clone2).on('input', function (e) {
    this.value = isCommon_Address($(this));
  });
  $('.postal-code', clone2).on('input', function (e) {
    this.value = isNumbers($(this));
  });
  var firstlist = unitval
  var cid = firstlist.country_id;
  var gid = firstlist.geography_id;
  var unitlts = loadupdateunitlocation(gid);
  loadglevelsupdate(cid, 'glevel-' + countryByCount + '-' + unit_second_cnt);

  //loadIndustry('industry-'+countryByCount+'-'+1);
  $('.glevel-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + unitlts.level_id + ']').attr('selected', 'selected');
  $('.unitlocation-' + countryByCount + '-' + unit_second_cnt).val(unitlts.gname);
  $('.unitlocation-ids-' + countryByCount + '-' + unit_second_cnt).val(gid);
  $('.full-location-list-' + countryByCount + '-' + unit_second_cnt).text(unitlts.mapping);
  $('.unit-id-' + countryByCount + '-'+unit_second_cnt).val(firstlist.unit_id);
  $('.unit-code-' + countryByCount + '-' + unit_second_cnt).val(firstlist.unit_code);
  $('.unit-name-' + countryByCount + '-'+unit_second_cnt).val(firstlist.unit_name);
  //$('.industry-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + firstlist.industry_id + ']').attr('selected', 'selected');
  $('.unit-address-' + countryByCount + '-' + unit_second_cnt).val(firstlist.unit_address);
  $('.postal-code-' + countryByCount + '-' + unit_second_cnt).val(firstlist.postal_code);
  var domainsListArray = firstlist.domain_ids;
  $('.domain-' + countryByCount + '-' + unit_second_cnt).val(domainsListArray);
  $('.domainselected-' + countryByCount + '-' + unit_second_cnt).val(domainsListArray.length + ' Selected');
  loaddomain('domain-' + countryByCount + '-' + unit_second_cnt);

  var orgtypeArray = firstlist.i_ids;
  $('.orgtype-' + countryByCount + '-' + unit_second_cnt).val(orgtypeArray);
  $('.orgtype-' + countryByCount + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');
  industrytype('industry-' + countryByCount + '-' + unit_second_cnt);

  if (firstlist.is_active == true) {
    $('.activedclass-' + countryByCount + '-' + unit_second_cnt).text('Active');
  } else {
    var classnamec = 'imgactivedclass-' + countryByCount + '-' + unit_second_cnt;
    $('.activedclass-' + countryByCount + '-' + unit_second_cnt).html('<img src="/images/icon-inactive.png" onclick="reactiviteunit(this, \'' + firstlist.unit_id + '\', \'' + clientunitId + '\');">');
  }
  if (firstlist.approve_status == "1") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Pending');
  }
  else if (firstlist.approve_status == "2") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Approved');
  }
  else if (firstlist.approve_status == "0") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Rejected');
  }
}

function addcountryrowupdate(unitval, unit_start_cnt, unit_second_cnt)
{
  alert("with division/category");
  console.log("div start:"+unit_start_cnt);
  console.log("div end:"+unit_second_cnt);
  var countryByCount = unit_start_cnt;
  var divCountryAddRow = $('#templates .grid-table');
  var clone4 = divCountryAddRow.clone();
  $('.btable', clone4).addClass('table-' + countryByCount);
  $('.countryval', clone4).addClass('countryval-' + countryByCount);
  $('.country', clone4).addClass('country-' + countryByCount);
  $('.autocompleteview', clone4).addClass('autocompleteview-' + countryByCount);
  $('.ulist-text', clone4).addClass('ulist-text-' + countryByCount);
  $('.divisioncnt', clone4).addClass('divisioncnt-' + countryByCount + '-' + unit_second_cnt);
  $('.division-id', clone4).addClass('division-id-' + countryByCount + '-' + unit_second_cnt);
  $('.division-name', clone4).addClass('division-name-' + countryByCount + '-' + unit_second_cnt);
  $('.category-name', clone4).addClass('category-name-' + countryByCount + '-' + unit_second_cnt);
  $('.active_cnt', clone4).addClass('active_cnt-' + countryByCount + '-' + unit_second_cnt);
  $('.unitcnt', clone4).addClass('unitcnt-' + countryByCount + '-' + unit_second_cnt);
  $('.sno', clone4).addClass('sno-' + countryByCount + '-' + unit_second_cnt);
  $('.geography-levels', clone4).addClass('glevel-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-location', clone4).addClass('unitlocation-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-location-ids', clone4).addClass('unitlocation-ids-' + countryByCount + '-' + unit_second_cnt);
  $('.auto-complete-unit-location', clone4).addClass('auto-complete-unit-location-' + countryByCount + '-' + unit_second_cnt);
  $('.unitlocationlist-text', clone4).addClass('unitlocationlist-text-' + countryByCount + '-' + unit_second_cnt);
  $('.full-location-list', clone4).addClass('full-location-list-' + countryByCount + '-' + unit_second_cnt);
  $('.unitcode-checkbox', clone4).addClass('unitcode-checkbox-' + countryByCount);
  $('.unit-code', clone4).addClass('unit-code-' + countryByCount);
  $('.unit-code', clone4).addClass('unit-code-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-name', clone4).addClass('unit-name-' + countryByCount + '-' + unit_second_cnt);
  $('.unit-address', clone4).addClass('unit-address-' + countryByCount + '-' + unit_second_cnt);
  $('.postal-code', clone4).addClass('postal-code-' + countryByCount + '-' + unit_second_cnt);
  $('.domain-list', clone4).addClass('domain-list-' + countryByCount + '-' + unit_second_cnt);
  $('.domainselected', clone4).addClass('domainselected-' + countryByCount + '-' + unit_second_cnt);
  $('.domain', clone4).addClass('domain-' + countryByCount + '-' + unit_second_cnt);
  $('.domain-selectbox-view', clone4).addClass('domain-selectbox-view-' + countryByCount + '-' + unit_second_cnt);
  $('.ul-domain-list', clone4).addClass('ul-domain-list-' + countryByCount + '-' + unit_second_cnt);

  $('.orgtype-list', clone4).addClass('orgtype-list-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtypeselected', clone4).addClass('orgtypeselected-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtype', clone4).addClass('orgtype-' + countryByCount + '-' + unit_second_cnt);
  $('.orgtype-selectbox-view', clone4).addClass('orgtype-selectbox-view-' + countryByCount + '-' + unit_second_cnt);
  $('.ul-orgtype-list', clone4).addClass('ul-orgtype-list-' + countryByCount + '-' + unit_second_cnt);
  $('.add-unit-row img', clone4).addClass('table-addunit-' + countryByCount);
  $('.tbody-unit-list', clone4).addClass('tbody-unit-' + countryByCount);
  $('.no-of-units', clone4).addClass('no-of-units-' + countryByCount);
  $('.activedclass', clone4).addClass('activedclass-' + countryByCount + '-' + unit_second_cnt);
  $('.approveclass', clone4).addClass('approveclass-' + countryByCount + '-' + unit_second_cnt);
  $('#unitcount').val(unit_second_cnt);
  //$('#countrycount').val(1);
  $('.unit-error-msg', clone4).addClass('unit-error-msg-' + countryByCount);
  $('.add-country-unit-list').append(clone4);
  //industrytype('industry-' + countryByCount + '-' + 1);
  $('.no-of-units-' + countryByCount).val(countryByCount);
  $('.sno-' + countryByCount + '-' + unit_second_cnt).text(unit_second_cnt);
  $('.divisioncnt-'+ countryByCount + '-' + unit_second_cnt).val(countryByCount);
  $('.unitcnt-'+ countryByCount + '-' + unit_second_cnt).val(unit_second_cnt);
  if (countryByCount != 1) {
    $('.unitcode-checkbox-' + countryByCount).hide();
  }
  $('.unit-code', clone4).on('input', function (e) {
    this.value = isCommon_Unitcode($(this));
  });
  $('.unit-name', clone4).on('input', function (e) {
    this.value = isCommon($(this));
  });
  $('.unit-address', clone4).on('input', function (e) {
    this.value = isCommon_Address($(this));
  });
  $('.postal-code', clone4).on('input', function (e) {
    this.value = isNumbers($(this));
  });
  var firstlist = unitval
  var cid = firstlist.country_id;

  //load division
  console.log("division det")
  console.log(firstlist.division_id)
  if(firstlist.division_id != null)
  {
    console.log("division det")
    loadDivision();
    $('.division-id-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + firstlist.division_id + ']').attr('selected', 'selected');
  }
  if(firstlist.category_name != '')
  {
    $('.category-name-' + unit_start_cnt + '-' + unitcount).val(unitval.category_name);
  }

  var gid = firstlist.geography_id;
  var unitlts = loadupdateunitlocation(gid);
  loadglevelsupdate(cid, 'glevel-' + countryByCount + '-' + unit_second_cnt);
  console.log("level id:"+unitlts.level_id)
  console.log($('.glevel-' + countryByCount + '-' + unit_second_cnt));

  //loadIndustry('industry-'+countryByCount+'-'+1);
  $('.glevel-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + unitlts.level_id + ']').attr('selected', 'selected');
  $('.unitlocation-' + countryByCount + '-' + unit_second_cnt).val(unitlts.gname);
  $('.unitlocation-ids-' + countryByCount + '-' + unit_second_cnt).val(gid);
  $('.full-location-list-' + countryByCount + '-' + unit_second_cnt).text(unitlts.mapping);
  $('.unit-id-' + countryByCount + '-'+unit_second_cnt).val(firstlist.unit_id);
  $('.unit-code-' + countryByCount + '-' + unit_second_cnt).val(firstlist.unit_code);
  $('.unit-name-' + countryByCount + '-'+unit_second_cnt).val(firstlist.unit_name);
  //$('.industry-' + countryByCount + '-' + unit_second_cnt + ' option[value=' + firstlist.industry_id + ']').attr('selected', 'selected');
  $('.unit-address-' + countryByCount + '-' + unit_second_cnt).val(firstlist.unit_address);
  $('.postal-code-' + countryByCount + '-' + unit_second_cnt).val(firstlist.postal_code);

  var domainsListArray = firstlist.domain_ids;
  $('.domain-' + countryByCount + '-' + unit_second_cnt).val(domainsListArray);
  $('.domainselected-' + countryByCount + '-' + unit_second_cnt).val(domainsListArray.length + ' Selected');
  loaddomain('domain-' + countryByCount + '-' + unit_second_cnt);

  var orgtypeArray = firstlist.i_ids;
  $('.orgtype-' + countryByCount + '-' + unit_second_cnt).val(orgtypeArray);
  $('.orgtypeselected-' + countryByCount + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');
  //$('.orgtype-selectbox-view-' + countryByCount + '-' + unit_second_cnt).css('display', 'none');
  industrytype('industry-' + countryByCount + '-' + unit_second_cnt);
  if (firstlist.is_active == true) {
    $('.activedclass-' + countryByCount + '-' + unit_second_cnt).text('Active');
  } else {
    var classnamec = 'imgactivedclass-' + countryByCount + '-' + unit_second_cnt;
    $('.activedclass-' + countryByCount + '-' + unit_second_cnt).html('<img src="/images/icon-inactive.png" onclick="reactiviteunit(this, \'' + firstlist.unit_id + '\', \'' + clientunitId + '\');">');
  }
  if (firstlist.approve_status == "1") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Pending');
  }
  else if (firstlist.approve_status == "2") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Approved');
  }
  else if (firstlist.approve_status == "0") {
    $('.approveclass-' + countryByCount + '-' + unit_second_cnt).text('Rejected');
  }
}

//Submit Record -----------------------------------------------------------------------------------------

$('#btn-clientunit-submit').click(function ()
{
  alert("division_cnt:"+division_cnt);
  clearMessage();
  var clientunitIdValue = $('#client-unit-id').val();
  var groupNameValue = $('#group-select').val();
  var businessgrouptextValue = $('#businessgroup-text').val();
  var businessgroupValue = $('#businessgroup-select').val();
  var businessgroupName = $('#businessgroup-select :selected').text();
  var legalEntityValue = $('#entity-select').val();
  var lentitytextValue = $('#entity-text').val().trim();
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
    if (lentitytextValue.length == 0) {
      if (legalEntityValue.length == 0) {
        displayMessage(message.legalentity_new);
        return false;
      }
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
    if (businessgrouptextValue == '') {
      bgIdValue = parseInt(businessgroupValue);
      if (businessgroupValue != '') {
        bgNameValue = businessgroupName;
      } else {
        bgNameValue = null;
      }
    } else {
      bgIdValue = null;
      bgNameValue = businessgrouptextValue;
    }
    var legalEntity;
    var leIdValue;
    var leNameValue;
    if (lentitytextValue == '') {
      leIdValue = parseInt(legalEntityValue);
      if (legalEntityValue != '') {
        leNameValue = legalEntityName;
      } else {
        leNameValue = null;
      }
    } else {
      leIdValue = null;
      leNameValue = lentitytextValue;
    }
    var division;
    var divIdValue;
    var divNameValue;

    var category=null;

    var units = [];
    var div_dict = [];
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
      unit_cnt = $('.unitcnt-'+ i + '-' + 1).val();
      if($('.category-name-' + i + '-' + 1).val()!='')
      {
        category = $('.category-name-' + i + '-' + 1).val();
      }
      else
      {
        category = null;
      }
      alert("categoryName:"+category);
      div_arr = mirror.getDivisionDict(divIdValue, divNameValue, category, 1, parseInt(unit_cnt));
      div_dict.push(div_arr);


      if(unit_cnt > 0)
      {
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
          unitIndustryId = $('.orgtype-' + i + '-' + j).val();
          //unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();
          unitdomain = $('.domain-' + i + '-' + j).val();
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
              var arrayDomainsVal = unitdomain.split(',');
              var arrayDomains = [];
              for (var m = 0; m < arrayDomainsVal.length; m++) {
                arrayDomains[m] = parseInt(arrayDomainsVal[m]);
              }
              var domainsVal = arrayDomains;

              //Organization Multiselect
              var arrayOrgtypeVal = unitIndustryId.split(',');
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
    alert("units length:"+units.length);
    mirror.saveClient(parseInt(groupNameValue), parseInt(bgIdValue), leIdValue, parseInt(countryVal), div_dict, units, function (error, response) {
      if (error == null) {
        alert(message.unit_save);
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
    var businessgrouptextValue = $('#businessgroup-text').val().trim();
    var businessgroupidupdate = $('#businessgroup-update-id').val();
    var businessgrouptext = $('#businessgroup-select :selected').text().trim();
    var businessgroupid = $('#businessgroup-select').val();
    var lentitytextValue = $('#entity-text').val().trim();
    var legalentityidupdate = $('#legalentity-update-id').val();
    var legalentityid = $('#entity-select').val();
    var legalentitytext = $('#entity-select :selected').text();
    var countryVal = $('#country-id').val();
    /*var divisiontextValue = $('#division-text').val().trim();
    var divisionidupdate = $('#division-update-id').val();
    var divisionid = $('#division-select').val();
    var divisiontext = $('#division-select :selected').text();*/

    if (businessgrouptextValue == '' && businessgroupidupdate != '') {
      displayMessage(message.businessgroup_required);
      return;
    }
    else {
      businessGroup = null;
    }

    if (lentitytextValue == '' && legalentityidupdate != '') {
      displayMessage(message.legalentity_required);
      return;
    }

    if(countryVal == ''){
      displayMessage(message.country_required);
      return;
    }

    var division;
    var divIdValue;
    var divNameValue;

    var category=null;

    var units = [];
    var div_dict = [];
    var unitarr = [];
    alert("division cnt:"+division_cnt);
    alert("unit cnt:"+unit_cnt);

    for (var i=1; i<= division_cnt; i++)
    {

      unit_cnt = $('.unitcnt-'+ i + '-' + 1).val();
    }
  }
//main loop -- end
});

function reactiviteunit(thisval, unitid, clientid) {
  $('#unitidval').val(unitid);
  $('#clientidval').val(clientid);
  window.scrollTo(0, 0);
  $('.overlay').css('visibility', 'visible');
  $('.overlay').css('opacity', '1');
  $('.popup-error-msg').html('');
  $('input[name=password]').html('');
  $('#password').html('');
}
$('.close').click(function () {
  $('#unitidval').val('');
  $('#clientidval').val('');
  $('.overlay').css('visibility', 'hidden');
  $('.overlay').css('opacity', '0');
});
function unit_close() {
  var unitidval = $('#unitidval').val();
  var clientidval = $('#clientidval').val();
  var password = $('#password').val();
  if (password == '') {
    $('.popup-error-msg').html('Enter password');
  } else {
    function onSuccess(data) {
      custom_alert('Unit \'' + data.unit_name + '\'\' has been reactivated successfully.\n New Unit code for the unit is \'' + data.unit_code + '\' \n You need to Assign statutory for this unit, \n for the client to access');
      $('#unitidval').val('');
      $('#clientidval').val('');
      $('.overlay').css('visibility', 'hidden');
      $('.overlay').css('opacity', '0');
      initialize();
    }
    function onFailure(error) {
      if (error == 'InvalidPassword') {
        $('.popup-error-msg').html('Enter Correct password');
      } else {
        $('.popup-error-msg').html(error);
      }
      $('#password').val('');
    }
    mirror.reactivateUnit(parseInt(clientidval), parseInt(unitidval), password, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
}
// function reactiviteunit(thisval, unitid, clientid){
//     var classval = $(thisval).attr("class");
// }
//Active or inactive Client Unit List
function clientunit_active(clientunitId, lentityId, divisionId, isActive) {
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        function onSuccess(data) {
          initialize();
        }
        function onFailure(error) {
          displayMessage(error);
        }
        mirror.changeClientStatus(parseInt(clientunitId), parseInt(lentityId), divisionId, isActive, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      },
      Cancel: function () {
        $(this).dialog('close');
      }
    },
    open: function () {
      $('.warning-message').html(msgstatus);
    }
  });
}
//Search Client name ----------------------------------------------------------------------------------------------
$('#search-clientunit-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.clientunit-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
});
function hidemenu(classname) {
  var lastClass = classname.split(' ').pop();
  var ccount = lastClass.split('-').pop();
  $('.autocompleteview-' + ccount).css('display', 'none');
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

//autocomplete function callback
function activate_text(element, callback) {
  $('.ac-textbox').hide();
  var ac_id = $(element).attr('id');
  var ac_name = $(element).text();
  var ac_result = [
    ac_id,
    ac_name
  ];
  console.log(ac_result);
  callback(ac_result);
}
function activate_text_arrow(ac_id, ac_name, callback) {
  $('.ac-textbox').hide();
  var ac_result = [
    ac_id,
    ac_name
  ];
  console.log(ac_result);
  callback(ac_result);
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

  $('#country-name').val(val[1]);
  $('#country-id').val(val[0]);
  $('#country-name').focus();
}

function loadauto_countrytext(e, textval, callback) {
  $('#country-id').val('');
  $('#ac-country').show();
  $('#ac-country ul').empty();
  var groupId;

  if ($('#client-unit-id').val() != '') {
    groupId = $('#client-unit-id').val();
  } else if ($('#client-unit-id').val() == '') {
    groupId = $('#group-select').val();
  }
  if (groupId == '' || groupId == 0) {
    displayMessage(message.group_required);
  } else {
    var arrayCountry = [];
    for (var i in groupList) {
      if (groupList[i].client_id == groupId) {
        arrayCountry = groupList[i].country_ids;
      }
    }
  }

  var countries = countryFulList;
  if (textval.length > 0) {
    for (var i in countries) {
      for (var j = 0; j < arrayCountry.length; j++) {
        if (arrayCountry[j] == countries[i].country_id) {
          if (~countries[i].country_name.toLowerCase().indexOf(textval.toLowerCase()) && countries[i].is_active == 1)
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
  onArrowKey_Client(e, 'ac-textbox', 'country', callback);

////////
  /*$("." + divclassval).css('display', 'block');
  $('.'+ listclassval).empty();
  var groupId;
  if ($('#client-unit-id').val() != '') {
    groupId = $('#client-unit-id').val();
  } else if ($('#client-unit-id').val() == '') {
    groupId = $('#group-select').val();
  }
  if (groupId == '') {
    displayMessage(message.group_required);
  } else {
    var arrayCountry = [];
    for (var i in groupList) {
      if (groupList[i].client_id == groupId) {
        arrayCountry = groupList[i].country_ids;
      }
    }
  }
  var countries = countryFulList;
  var suggestions = [];

  if (textval.length > 0) {
    for (var i in countries) {
      for (var j = 0; j < arrayCountry.length; j++) {
        if (arrayCountry[j] == countries[i].country_id) {
          if (~countries[i].country_name.toLowerCase().indexOf(textval.toLowerCase()) && countries[i].is_active == 1)
          {
            alert(countries[i].country_name);
            var obj = $(".country-list-drop-down li");
            console.log(obj);
            var clone = obj.clone();
            clone.attr("id", countries[i].country_id);
            clone.click(function(){
                activate_text(this, txtclassval, 'country');
            });
            clone.text(countries[i].country_name);
            $('.'+listclassval).append(clone);
          }
        }
      }
    }
  }
  console.log('.'+listclassval)
  onArrowKey_Client(e, divclassval, 'ac-textbox', 'country');*/
}

//set selected autocomplte value to textbox and geographylevel list
function hideunitlocation(classname) {
  var lastClass = classname.split(' ').pop();
  $('.' + lastClass).css('display', 'none');
}
function activate_unitlocaion(element, ccount, mappingname) {
  var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $('.unitlocation' + ccount).val(checkname);
  $('.unitlocation-ids' + ccount).val(checkval);
  $('.full-location-list' + ccount).html('<br>' + mappingname.replace(/##/gi, '"'));
}
//autocomplete location
function loadlocation(textval, classval, e) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[1] + '-' + ccount[2];
  var glevelval = $('.glevel' + countval).val();
  $('.auto-complete-unit-location' + countval).css('display', 'block');
  var suggestions = [];
  $('.unitlocationlist-text' + countval).empty();
  if (textval.length > 0) {
      for (var glist in geographyList) {
        console.log("active:"+geographyList[glist].is_active)
        if (geographyList[glist].level_id == glevelval) {
          if (~geographyList[glist].geography_name.toLowerCase().indexOf(textval.toLowerCase()) && geographyList[glist].is_active == 1)
            suggestions.push([
              geographyList[glist].geography_id,
              geographyList[glist].geography_name,
              geographyList[glist].mapping
            ]);
        }
      }

    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '" onclick="activate_unitlocaion(this,\'' + countval + '\', \'' + suggestions[i][2].replace(/"/gi, '##') + '\')">' + suggestions[i][1] + '</li>';
    }
    console.log("str:"+str)
    $('.unitlocationlist-text' + countval).append(str);
    //$('.unitlocation-ids'+countval).val('');
    onArrowKey_Client(e, 'unitlocationlist-text' + countval, countval, 'unit');
  }
}
function domainunionclientdomainList(classval) {
  var finalObj;
  var d = '';
  var cd = '';
  var cdnew = '';
  var editdomainval = [];
  d = domainList;
  cd = clientdomainList;
  if ($('.domain' + classval).val() != '') {
    editdomainval = $('.domain' + classval).val().split(',');
  }
  var result = {};
  cdnew = [];
  var arrayDomains = [];
  for (var i = 0; i < editdomainval.length; i++) {
    arrayDomains[i] = parseInt(editdomainval[i]);
  }
  $.each(cd, function (key) {
    if ($.inArray(cd[key].domain_id, arrayDomains) != -1) {
      cdnew[key] = cd[key];
    }
  });
  var finalObj1 = [];
  finalObj1 = d.concat(cdnew);
  var dupes = {};
  finalObj = [];
  $.each(finalObj1, function (i, el) {
    if (el != null) {
      if (!dupes[el.domain_id]) {
        dupes[el.domain_id] = true;
        finalObj.push(el);
      }
    }
  });
  //});
  return finalObj;
}
function checkclientdomain(domainid, classcount) {
  var returnval = null;
  var arrayDomains = [];
  var editdomainval;
  editdomainval = $('.domain' + classcount).val().split(',');
  for (var i = 0; i < editdomainval.length; i++) {
    arrayDomains[i] = parseInt(editdomainval[i]);
  }
  if ($.inArray(domainid, arrayDomains) != -1) {
    returnval = 1;
  }
  return returnval;
}
function checkdomainforadd(clientdomainsid, domainid) {
  var returnval = null;
  if ($.inArray(domainid, clientdomainsid) != -1) {
    returnval = 1;
  }
  return returnval;
}
function checkdomain(domainid, classcount) {
  var returnval = null;
  $.each(domainList, function (key, value) {
    if (value.domain_id == domainid) {
      returnval = 1;
    }
  });
  return returnval;
}
function hidedomain(classval) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[3] + '-' + ccount[4];
  $('.domain-selectbox-view' + countval).css('display', 'none');
}
function hideorgtype(classval) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[3] + '-' + ccount[4];
  console.log('.orgtype-selectbox-view' + countval);
  $('.orgtype-selectbox-view' + countval).css('display', 'none');
}
//Load Domain  for Unit under country
function loaddomain(classval) {
  console.log(classval);
  var lastClass = classval.split(' ').pop();
  console.log("lc:"+lastClass);
  var ccount = lastClass.split('-');
  console.log("cc:"+ccount);
  var countval = '-' + ccount[1] + '-' + ccount[2];
  $('.domain-selectbox-view' + countval).css('display', 'block');
  var getClientid;
  if (($('#client-unit-id').val() == '') || ($('#client-unit-id').val() == 0)) {
    getClientid = $('#group-select').val();
    console.log("client unit id null:"+getClientid)
  } else {
    getClientid = $('#client-unit-id').val();
    console.log("client unit id not null:"+getClientid)
  }
  console.log('.domain' + countval);
  var clientdomainsid;
  $.each(groupList, function (key, val) {
    if (val.client_id == getClientid) {
      clientdomainsid = val.domain_ids;
    }
  });
  console.log("client domain val:"+clientdomainsid);
  var editdomainval = [];
  if ($('.domain' + countval).val() != '') {
    //$('.domain-selectbox-view' + countval).css('display', 'none');
    editdomainval = $('.domain' + countval).val().split(',');
  }
  console.log("domains edit:"+editdomainval)

  if (($('#client-unit-id').val() == '') || ($('#client-unit-id').val() == 0)) {
    var domains = domainList;
    $('.ul-domain-list' + countval).empty();
    var str = '';
    for (var i in domains) {
      var selectdomainstatus = '';
      if(editdomainval.length > 0)
      {
        for (var j = 0; j < editdomainval.length; j++) {
          if (editdomainval[j] == domains[i].domain_id) {
            selectdomainstatus = 'checked';
          }
        }
      }
      var domainId = parseInt(domains[i].domain_id);
      var domainName = domains[i].domain_name;
      if (checkdomainforadd(clientdomainsid, domainId) == 1) {
        if (selectdomainstatus == 'checked') {
          str += '<li id="' + domainId + '" class="active_selectbox' + countval + ' active" onclick="activate_domain_element(this, \'' + countval + '\')" >' + domainName + '</li> ';
        } else {
          str += '<li id="' + domainId + '" onclick="activate_domain_element(this, \'' + countval + '\')" >' + domainName + '</li> ';
        }
      }
    }
  } else if ($('#client-unit-id').val() != '') {
    var domains = domainunionclientdomainList(countval);
    //console.log(domains);
    $('.ul-domain-list' + countval).empty();
    var str = '';
    for (var i in domains) {
      var selectdomainstatus = '';
      for (var j = 0; j < editdomainval.length; j++) {
        if (editdomainval[j] == domains[i].domain_id) {
          selectdomainstatus = 'checked';
        }
      }
      var domainId = parseInt(domains[i].domain_id);
      var domainName = domains[i].domain_name;
      var ccdd = checkclientdomain(domainId, countval);
      var cdd = checkdomain(domainId, countval);
      if (checkdomainforadd(clientdomainsid, domainId) == 1) {
        if (ccdd == 1 && cdd == 1) {
          if (selectdomainstatus == 'checked') {
            str += '<li id = "' + domainId + '" class="active_selectbox' + countval + ' active" onclick="activate_domain_element(this, \'' + countval + '\')" >' + domainName + '</li> ';
          } else {
            str += '<li id="' + domainId + '" onclick="activate_domain_element(this, \'' + countval + '\')" >' + domainName + '</li> ';
          }
        } else if (ccdd != 1 && cdd == 1) {
          str += '<li id="' + domainId + '" onclick="activate_domain_element(this, \'' + countval + '\')" >' + domainName + '</li> ';
        } else if (ccdd == 1 && cdd != 1) {
          if (selectdomainstatus == 'checked') {
            str += '<li id="' + domainId + '" class="active_selectbox' + countval + ' active deactivate" >' + domainName + '</li> ';
          } else {
            str += '<li id="' + domainId + '" class="deactivate" >' + domainName + '</li> ';
          }
        }
      }  // if(selectdomainstatus == 'checked'){
         //     str += '<li id="'+domainId+'" class="active_selectbox'+countval+' active" onclick="activate(this,\''+countval+'\' )" >'+domainName+'</li> ';
         // }else{
         //     str += '<li id="'+domainId+'" onclick="activate(this,\''+countval+'\')" >'+domainName+'</li> ';
         // }
    }
  }
  console.log("domain str:"+str)
  $('.ul-domain-list' + countval).append(str);
  $('.domainselected' + countval).val(editdomainval.length + ' Selected');
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
var chosen_unit = '';
function loaddomain_ms(e, classval) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[1] + '-' + ccount[2];
  onArrowKeyUnit(e, 'ul-domain-list' + countval, countval);
}
function loadorgtype_ms(e, classval) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[1] + '-' + ccount[2];
  onArrowKeyUnit(e, 'ul-orgtype-list' + countval, countval);
}
function activate_domain(count) {
  var selids = '';
  var selNames = '';
  var totalcount = $('.active_selectbox' + count).length;
  $('.active_selectbox' + count).each(function (index, el) {
    if (index === totalcount - 1) {
      selids = selids + el.id;
    } else {
      selids = selids + el.id + ',';
    }
  });
  $('.domainselected' + count).val(totalcount + ' Selected');
  $('.domain' + count).val(selids);
}
function activate_orgtype(count) {
  var selids = '';
  var selNames = '';
  var totalcount = $('.active_org_selectbox' + count).length;
  $('.active_org_selectbox' + count).each(function (index, el) {
    if (index === totalcount - 1) {
      selids = selids + el.id;
    } else {
      selids = selids + el.id + ',';
    }
  });
  console.log("industry selected:"+selids);
  $('.orgtypeselected' + count).val(totalcount + ' Selected');
  $('.orgtype' + count).val(selids);
}
//check & uncheck process
function activate_domain_element(element, count) {
  var chkstatus = $(element).attr('class');
  console.log("chkstatus:"+element);
  if (chkstatus == 'active_selectbox' + count + ' active') {
    $(element).removeClass('active_selectbox' + count);
    $(element).removeClass('active');
  } else {
    $(element).addClass('active_selectbox' + count);
    $(element).addClass('active');
  }
  activate_domain(count);
}

function activate_orgtype_element(element, count) {
  var chkstatus = $(element).attr('class');
  console.log("chkstatus:"+element);
  if (chkstatus == 'active_org_selectbox' + count + ' active') {
    $(element).removeClass('active_org_selectbox' + count);
    $(element).removeClass('active');
  } else {
    $(element).addClass('active_org_selectbox' + count);
    $(element).addClass('active');
  }
  activate_orgtype(count);
}


function divisionExistingChecking(str) {
  if (str == 'New') {
    $('#division-text').show();
    $('#division-select').hide();
    $('#division-new').hide();
    $('#division-existing').show();
    $('#division-text').val('');
    $('#division-select').val('');
  }
  if (str == 'Cancel') {
    $('#division-text').hide();
    $('#division-select').show();
    $('#division-new').show();
    $('#division-existing').hide();
    $('#division-text').val('');
    $('#division-select').val('');
    $('#division-select').find('option').not(':first').remove();
    loadDivision();
  }
}
function legalEntityExistingChecking(str) {
  if (str == 'New') {
    $('#entity-text').show();
    $('#entity-select').hide();
    $('#entity-new').hide();
    $('#entity-existing').show();
    $('#division-text').show();
    $('#division-select').hide();
    $('#division-new').hide();
    $('#division-existing').hide();
    $('#division-text').val('');
    $('#division-select').val('');
    $('#entity-text').val('');
    $('#entity-select').val('');
  }
  if (str == 'Cancel') {
    $('#entity-text').hide();
    $('#entity-select').show();
    $('#entity-new').show();
    $('#entity-existing').hide();
    $('#division-text').hide();
    $('#division-select').show();
    $('#division-new').show();
    $('#division-existing').hide();
    $('#division-text').val('');
    $('#division-select').val('');
    $('#entity-text').val('');
    $('#entity-select').val('');
    $('#entity-select').find('option').not(':first').remove();
    $('#division-select').find('option').not(':first').remove();
    loadLegalEntity();
  }
}
function businessGroupExistingChecking(str) {
  if (str == 'New') {
    $('#businessgroup-text').show();
    $('#businessgroup-select').hide();
    $('#businessgroup-new').hide();
    $('#businessgroup-existing').show();
    $('#entity-text').show();
    $('#entity-select').hide();
    $('#entity-new').hide();
    $('#entity-existing').hide();
    $('#division-text').show();
    $('#division-select').hide();
    $('#division-new').hide();
    $('#division-existing').hide();
    $('#division-text').val('');
    $('#division-select').val('');
    $('#entity-text').val('');
    $('#entity-select').val('');
    $('#businessgroup-text').val('');
    $('#businessgroup-select').val('');
  }
  if (str == 'Cancel') {
    $('#businessgroup-text').hide();
    $('#businessgroup-select').show();
    $('#businessgroup-new').show();
    $('#businessgroup-existing').hide();
    $('#entity-text').hide();
    $('#entity-select').show();
    $('#entity-new').show();
    $('#entity-existing').hide();
    $('#division-text').hide();
    $('#division-select').show();
    $('#division-new').show();
    $('#division-existing').hide();
    $('#division-text').val('');
    $('#division-select').val('');
    $('#entity-text').val('');
    $('#entity-select').val('');
    $('#businessgroup-text').val('');
    $('#businessgroup-select').val('');
    $('#businessgroup-select').find('option').not(':first').remove();
    $('#entity-select').find('option').not(':first').remove();
    $('#division-select').find('option').not(':first').remove();
    loadBusinessGroups();
  }
}
$(function () {
  initialize();
});
$(document).find('.js-filtertable').each(function () {
  $(this).filtertable().addFilter('.js-filter');
});
$('#businessgroup-text').on('input', function (e) {
  this.value = isCommon($(this));
});
$('#entity-text').on('input', function (e) {
  this.value = isCommon($(this));
});
$('#division-text').on('input', function (e) {
  this.value = isCommon($(this));
});
