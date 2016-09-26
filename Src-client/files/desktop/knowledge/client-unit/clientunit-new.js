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
    groupList = data.group_companies;
    businessGroupList = data.business_groups;
    legalEntitiesList = data.legal_entities;
    divisionList = data.divisions;
    countryFulList = data.countries;
    geographyLevelList = data.geography_levels;
    geographyList = data.geographies;
    industryList = data.industries;
    domainList = data.domains;
    unitList = data.units;
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
  $('.tbody-clientunit-list').find('tr').remove();
  var sno = 0;
  var getAllArrayValues = [];
  for (var i = 0; i < groupList.length; i++) {
    max[groupList[i].client_id] = groupList[i].no_of_units;
  }
  $.each(unitList, function (key, value) {
    var isActive = value.is_active;
    var unitId = value.unit_id;
    var unitVal = {};
    var clientId = value.client_id;
    var bgroupId = value.business_group_id;
    var lentitiesId = value.legal_entity_id;
    var divisionId = value.division_id;
    var tableRow = $('#templates .table-clientunit-list .table-row');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.group-name', clone).text(getGroupName(clientId));
    $('.business-group-name', clone).text(getBusinessGroupName(bgroupId));
    $('.legal-entity-name', clone).text(getLegalEntityName(lentitiesId));
    $('.division-name', clone).text(getDivisionName(divisionId));
    $('.edit-icon').attr('title', 'Edit');
    $('.edit-icon', clone).on('click', function () {
      clientunit_edit(clientId, bgroupId, lentitiesId, divisionId);
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
  $('.industry').find('option').not(':first').empty();
  $('.add-country-unit-list').empty();
  divisionExistingChecking('Cancel');
  legalEntityExistingChecking('Cancel');
  businessGroupExistingChecking('Cancel');
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
  $('#group-select').find('option:gt(0)').remove();
  $.each(groupsList, function (key, value) {
    var groupId = value.client_id;
    var groupName = value.group_name;
    //if (value.is_active == true) {
      $('#group-select').append($('<option value = "' + groupId + '">' + groupName + '</option>'));
    //}
  });
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
//Load Divisions ---------------------------------------------------------------------------------------------
function loadDivision() {
  var lentityId = $('#entity-select').val();
  $('#division-select').find('option:gt(0)').remove();
  alert(divisionList.length);
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
function loadupdateunitlocation(cid, gid) {
  var units = {};
  $.each(geographyList, function (key, val) {
    if (key == cid) {
      $.each(val, function (k, v) {
        if (v.geography_id == gid) {
          units.gname = v.geography_name;
          units.mapping = v.mapping;
          units.level_id = v.level_id;
        }
      });
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
    addcountryrownew();
  }
}
//Add Country Wise List ----------------------------------------------------------------------------------------
function addcountryrownew() {
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
      var divCountryAddRow = $('#templates .grid-table');
      var clone = divCountryAddRow.clone();
      $('.btable', clone).addClass('table-' + countryByCount);
      $('.countryval', clone).addClass('countryval-' + countryByCount);
      $('.country', clone).addClass('country-' + countryByCount);
      $('.autocompleteview', clone).addClass('autocompleteview-' + countryByCount);
      $('.ulist-text', clone).addClass('ulist-text-' + countryByCount);
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
      $('.industry', clone).addClass('industry-' + countryByCount + '-' + 1);
      $('.unit-address', clone).addClass('unit-address-' + countryByCount + '-' + 1);
      $('.postal-code', clone).addClass('postal-code-' + countryByCount + '-' + 1);
      $('.domain-list', clone).addClass('domain-list-' + countryByCount + '-' + 1);
      $('.domainselected', clone).addClass('domainselected-' + countryByCount + '-' + 1);
      $('.domain', clone).addClass('domain-' + countryByCount + '-' + 1);
      $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-' + countryByCount + '-' + 1);
      $('.ul-domain-list', clone).addClass('ul-domain-list-' + countryByCount + '-' + 1);
      $('.add-unit-row img', clone).addClass('table-addunit-' + countryByCount);
      $('.tbody-unit-list', clone).addClass('tbody-unit-' + countryByCount);
      $('.no-of-units', clone).addClass('no-of-units-' + countryByCount);
      $('.activedclass', clone).addClass('activedclass-' + countryByCount + '-' + 1);
      $('#unitcount').val(1);
      $('.unit-error-msg', clone).addClass('unit-error-msg-' + countryByCount);
      $('.add-country-unit-list').append(clone);
      industrytype('industry-' + countryByCount + '-' + 1);
      $('.no-of-units-' + countryByCount).val(1);
      $('.activedclass-' + countryByCount + '-' + 1).text('Active');
      if (countryByCount != 1) {
        $('.unitcode-checkbox-' + countryByCount).hide();
      }
      if ($('.unitcode-checkbox').is(':checked')) {
        $('.unit-code-' + countryByCount + '-' + 1).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
      }
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
  var tableclassname = $(str).parents('table').attr('class');
  var tableclass = tableclassname.split(' ');
  var countval = tableclass[1].split('-').pop();
  var tbodyclassname = $('.' + tableclass[1]).find('tbody:eq(1)').attr('class');
  var tbodyclasses = tbodyclassname.split(' ');
  var lastclassname = $('.' + tbodyclasses[1]).find('tr:last .geography-levels').attr('class');
  var lastClass = lastclassname.split(' ').pop();
  var lastClassval = parseInt(lastClass.split('-').pop());
  var divUnitAddRow = $('#templatesUnitRow .table-UnitRow-list .table-row');
  var clone1 = divUnitAddRow.clone();
  $('.geography-levels', clone1).addClass('glevel-' + countval + '-' + (lastClassval + 1));
  $('.unit-location', clone1).addClass('unitlocation-' + countval + '-' + (lastClassval + 1));
  $('.unit-location-ids', clone1).addClass('unitlocation-ids-' + countval + '-' + (lastClassval + 1));
  $('.auto-complete-unit-location', clone1).addClass('auto-complete-unit-location-' + countval + '-' + (lastClassval + 1));
  $('.unitlocationlist-text', clone1).addClass('unitlocationlist-text-' + countval + '-' + (lastClassval + 1));
  $('.full-location-list', clone1).addClass('full-location-list-' + countval + '-' + (lastClassval + 1));
  $('.unit-code', clone1).addClass('unit-code-' + countval);
  $('.unit-code', clone1).addClass('unit-code-' + countval + '-' + (lastClassval + 1));
  $('.unit-name', clone1).addClass('unit-name-' + countval + '-' + (lastClassval + 1));
  $('.industry', clone1).addClass('industry-' + countval + '-' + (lastClassval + 1));
  $('.unit-address', clone1).addClass('unit-address-' + countval + '-' + (lastClassval + 1));
  $('.postal-code', clone1).addClass('postal-code-' + countval + '-' + (lastClassval + 1));
  $('.domain-list', clone1).addClass('domain-list-' + countval + '-' + (lastClassval + 1));
  $('.domainselected', clone1).addClass('domainselected-' + countval + '-' + (lastClassval + 1));
  $('.domain', clone1).addClass('domain-' + countval + '-' + (lastClassval + 1));
  $('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-' + countval + '-' + (lastClassval + 1));
  $('.ul-domain-list', clone1).addClass('ul-domain-list-' + countval + '-' + (lastClassval + 1));
  $('.no-of-units-' + countval).val(parseInt($('.no-of-units-' + countval).val()) + 1);
  $('.activedclass', clone1).addClass('activedclass-' + countval + '-' + (lastClassval + 1));
  $('.' + tbodyclasses[1]).append(clone1);
  if ($('.unitcode-checkbox').is(':checked')) {
    $('.unit-code-' + countval + '-' + (lastClassval + 1)).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
    unitcodeautogenerateids++;
  }
  $('.activedclass-' + countval + '-' + (lastClassval + 1)).text('Active');
  industrytype('industry-' + countval + '-' + (lastClassval + 1));
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
    for (var glevel in geographyLevelList[countryid]) {
      var glevellist = geographyLevelList[countryid][glevel];
      $('.' + lastClass).append($('<option value = "' + glevellist.l_id + '">' + glevellist.l_name + '</option>'));
    }
  }
}
//Load Geography Levels -------------------------------------------------------------------------------------------
function loadglevels(classval) {
  alert(classval)
  var lastClass = classval.split(' ').pop();
  alert(classval.split(' ').pop());
  var checkval = lastClass.split('-');
  alert(checkval[1])
  var countryvalue = $('.countryval-' + checkval[1]).val();
  var countryid = $('.country-' + checkval[1]).val();
  if (countryvalue == '') {
    displayMessage(message.country_required);
  } else {
    $('.' + lastClass).find('option').not(':first').remove();
    for (var glevel in geographyLevelList[countryid]) {
      var glevellist = geographyLevelList[countryid][glevel];
      $('.' + lastClass).append($('<option value = "' + glevellist.l_id + '">' + glevellist.l_name + '</option>'));
    }
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
  //var lastClass = classval.split(' ').pop();
  //var lastClass = classval;
  //var checkval = lastClass.split('-');
  $('.' + classval).find('option').not(':first').remove();
  $('.' + classval).append($('<option value = "">Select</option>'));
  for (var industry in industryList) {
    $('.' + classval).append($('<option value = "' + industryList[industry].industry_id + '">' + industryList[industry].industry_name + '</option>'));
  }
}
//Edit client Unit -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, businessgroupId, legalentityId, divisionId) {
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
  $('#division-text').show();
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
  $('#division-select').find('option').not(':first').remove();
  $('.industry').find('option').not(':first').remove();
  checkunitscount = null;
  clearMessage();
  function onSuccess(data) {
    clientdomainList = data.client_domains;
    loadFormListUpdate(clientunitId, businessgroupId, legalentityId, divisionId);
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
function loadFormListUpdate(clientunitId, businessgroupId, legalEntityId, divisionId) {
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
  //Division
  if (divisionId != '') {
    loadDivision(legalEntityId);
    $('#division-update-id').val(divisionId);
    $('#division-text').val(getDivisionName(divisionId));  //$(".labeldivision").text(getDivisionName(divisionId));
                                                           //$('#division-select option[value = '+divisionId+']').attr('selected','selected');
  }
  if (divisionId == null) {
    $('#division-text').hide();  //$(".labeldivision").text('');
                                 //$('#division-select').append($('<option value = "">select</option>'));
  }
  //Load Countries
  $.each(unitList, function (unitkey, unitval) {
    if (unitval.client_id == clientunitId && unitval.business_group_id == businessgroupId && unitval.legal_entity_id == legalEntityId && unitval.division_id == divisionId) {
      var unitValues = unitval.units;
      $.each(unitValues, function (key, value) {
        var unitListVal = unitValues[key];
        var units = [];
        var j = 0;
        $.each(unitListVal, function (k, val) {
          units[j++] = val.unit_id;
        });
        addcountryrowupdate(clientunitId, businessgroupId, legalEntityId, divisionId, key, units, countryByCount, unitval.units);
        //add country by Unit
        countryByCount++;
      });
    }
  });
}
function addcountryrowupdate(clientunitId, businessgroupId, legalEntityId, divisionId, key, units, bycount, unitval) {
  alert("hi");
  var countryByCount = bycount;
  var divCountryAddRow = $('#templates .grid-table');
  var clone = divCountryAddRow.clone();
  $('.btable', clone).addClass('table-' + countryByCount);
  $('.countryval', clone).addClass('countryval-' + countryByCount);
  $('.country', clone).addClass('country-' + countryByCount);
  $('.autocompleteview', clone).addClass('autocompleteview-' + countryByCount);
  $('.ulist-text', clone).addClass('ulist-text-' + countryByCount);
  $('.geography-levels', clone).addClass('glevel-' + countryByCount + '-' + 1);
  $('.unit-location', clone).addClass('unitlocation-' + countryByCount + '-' + 1);
  $('.unit-location-ids', clone).addClass('unitlocation-ids-' + countryByCount + '-' + 1);
  $('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-' + countryByCount + '-' + 1);
  $('.unitlocationlist-text', clone).addClass('unitlocationlist-text-' + countryByCount + '-' + 1);
  $('.full-location-list', clone).addClass('full-location-list-' + countryByCount + '-' + 1);
  $('.unitcode-checkbox', clone).addClass('unitcode-checkbox-' + countryByCount);
  $('.unit-id', clone).addClass('unit-id-' + countryByCount + '-' + 1);
  $('.unit-code', clone).addClass('unit-code-' + countryByCount);
  $('.unit-code', clone).addClass('unit-code-' + countryByCount + '-' + 1);
  $('.unit-name', clone).addClass('unit-name-' + countryByCount + '-' + 1);
  $('.industry', clone).addClass('industry-' + countryByCount + '-' + 1);
  $('.unit-address', clone).addClass('unit-address-' + countryByCount + '-' + 1);
  $('.postal-code', clone).addClass('postal-code-' + countryByCount + '-' + 1);
  $('.domain-list', clone).addClass('domain-list-' + countryByCount + '-' + 1);
  $('.domainselected', clone).addClass('domainselected-' + countryByCount + '-' + 1);
  $('.domain', clone).addClass('domain-' + countryByCount + '-' + 1);
  $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-' + countryByCount + '-' + 1);
  $('.ul-domain-list', clone).addClass('ul-domain-list-' + countryByCount + '-' + 1);
  $('.add-unit-row img', clone).addClass('table-addunit-' + countryByCount);
  $('.tbody-unit-list', clone).addClass('tbody-unit-' + countryByCount);
  $('.no-of-units', clone).addClass('no-of-units-' + countryByCount);
  $('#unitcount').val(1);
  $('.unit-error-msg', clone).addClass('unit-error-msg-' + countryByCount);
  $('.activedclass', clone).addClass('activedclass-' + countryByCount + '-1');
  $('.add-country-unit-list').append(clone);
  $('.no-of-units-' + countryByCount).val(1);
  if (countryByCount != 1) {
    $('.unitcode-checkbox-' + countryByCount).hide();
  }
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
  var firstlist = unitval[key][0];
  $('.countryval-' + countryByCount).val(getCountryName(key));
  $('.countryval-' + countryByCount).attr('disabled', 'disabled');
  $('.country-' + countryByCount).val(key);
  var gid = firstlist.geography_id;
  var unitlts = loadupdateunitlocation(key, gid);
  loadglevelsupdate(key, 'glevel-' + countryByCount + '-' + 1);
  industrytype('industry-' + countryByCount + '-' + 1);
  //loadIndustry('industry-'+countryByCount+'-'+1);
  $('.glevel-' + countryByCount + '-' + 1 + ' option[value=' + unitlts.level_id + ']').attr('selected', 'selected');
  $('.unitlocation-' + countryByCount + '-' + 1).val(unitlts.gname);
  $('.unitlocation-ids-' + countryByCount + '-' + 1).val(gid);
  $('.full-location-list-' + countryByCount + '-' + 1).text(unitlts.mapping);
  $('.unit-id-' + countryByCount + '-1').val(firstlist.unit_id);
  $('.unit-code-' + countryByCount + '-' + 1).val(firstlist.unit_code);
  $('.unit-name-' + countryByCount + '-1').val(firstlist.unit_name);
  $('.industry-' + countryByCount + '-' + 1 + ' option[value=' + firstlist.industry_id + ']').attr('selected', 'selected');
  $('.unit-address-' + countryByCount + '-' + 1).val(firstlist.unit_address);
  $('.postal-code-' + countryByCount + '-' + 1).val(firstlist.postal_code);
  var domainsListArray = firstlist.domain_ids;
  $('.domain-' + countryByCount + '-' + 1).val(domainsListArray);
  $('.domainselected-' + countryByCount + '-' + 1).val(domainsListArray.length + ' Selected');
  if (firstlist.is_active == true) {
    $('.activedclass-' + countryByCount + '-' + 1).text('Active');
  } else {
    var classnamec = 'imgactivedclass-' + countryByCount + '-' + 1;
    $('.activedclass-' + countryByCount + '-' + 1).html('<img src="/images/icon-inactive.png" onclick="reactiviteunit(this, \'' + firstlist.unit_id + '\', \'' + clientunitId + '\');">');
  }
  // if($('.unit-id-'+countryByCount+'-1').val() != ''){
  //     unitcodeautogenerateids++;
  //     console.log("addcountryrowupdate=="+unitcodeautogenerateids);
  // }
  if (units != '') {
    var lastClassvalglobal = 2;
    var tbodyclassname = 'tbody-unit-' + countryByCount;
    var unitids = units.toString().split(',');
    for (var icount = 1; icount < unitids.length; icount++) {
      addUnitRowUpdate(clientunitId, businessgroupId, legalEntityId, divisionId, unitids[icount], tbodyclassname, lastClassvalglobal, countryByCount, unitval[key][icount], key);
      lastClassvalglobal++;
    }
  }
}
function addUnitRowUpdate(clientunitId, businessgroupId, legalEntityId, divisionId, unitid, tbodyclassname, lastClassval, countval, unitlist, countryid) {
  var divUnitAddRow = $('#templatesUnitRow .table-UnitRow-list .table-row');
  var clone1 = divUnitAddRow.clone();
  $('.geography-levels', clone1).addClass('glevel-' + countval + '-' + lastClassval);
  $('.unit-location', clone1).addClass('unitlocation-' + countval + '-' + lastClassval);
  $('.unit-location-ids', clone1).addClass('unitlocation-ids-' + countval + '-' + lastClassval);
  $('.auto-complete-unit-location', clone1).addClass('auto-complete-unit-location-' + countval + '-' + lastClassval);
  $('.unitlocationlist-text', clone1).addClass('unitlocationlist-text-' + countval + '-' + lastClassval);
  $('.full-location-list', clone1).addClass('full-location-list-' + countval + '-' + lastClassval);
  $('.unit-code', clone1).addClass('unit-code-' + countval);
  $('.unit-code', clone1).addClass('unit-code-' + countval + '-' + lastClassval);
  $('.unit-id', clone1).addClass('unit-id-' + countval + '-' + lastClassval);
  $('.unit-name', clone1).addClass('unit-name-' + countval + '-' + lastClassval);
  $('.industry', clone1).addClass('industry-' + countval + '-' + lastClassval);
  $('.unit-address', clone1).addClass('unit-address-' + countval + '-' + lastClassval);
  $('.postal-code', clone1).addClass('postal-code-' + countval + '-' + lastClassval);
  $('.domain-list', clone1).addClass('domain-list-' + countval + '-' + lastClassval);
  $('.domainselected', clone1).addClass('domainselected-' + countval + '-' + lastClassval);
  $('.domain', clone1).addClass('domain-' + countval + '-' + lastClassval);
  $('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-' + countval + '-' + lastClassval);
  $('.ul-domain-list', clone1).addClass('ul-domain-list-' + countval + '-' + lastClassval);
  $('.activedclass', clone1).addClass('activedclass-' + countval + '-' + lastClassval);
  $('.' + tbodyclassname).append(clone1);
  unitcodeautogenerateids++;
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
  $('.no-of-units-' + countval).val(parseInt($('.no-of-units-' + countval).val()) + 1);
  loadglevelsupdate(countryid, 'glevel-' + countval + '-' + lastClassval);
  var firstlist = unitlist;
  var gid = firstlist.geography_id;
  var unitlts = loadupdateunitlocation(countryid, gid);
  $('.glevel-' + countval + '-' + lastClassval + ' option[value=' + unitlts.level_id + ']').attr('selected', 'selected');
  $('.unitlocation-' + countval + '-' + lastClassval).val(unitlts.gname);
  $('.unitlocation-ids-' + countval + '-' + lastClassval).val(gid);
  $('.full-location-list-' + countval + '-' + lastClassval).text(unitlts.mapping);
  $('.unit-id-' + countval + '-' + lastClassval).val(firstlist.unit_id);
  $('.unit-code-' + countval + '-' + lastClassval).val(firstlist.unit_code);
  $('.unit-name-' + countval + '-' + lastClassval).val(firstlist.unit_name);
  industrytype('industry-' + countval + '-' + lastClassval);
  $('.industry-' + countval + '-' + lastClassval + ' option[value=' + firstlist.industry_id + ']').attr('selected', 'selected');
  $('.unit-address-' + countval + '-' + lastClassval).val(firstlist.unit_address);
  $('.postal-code-' + countval + '-' + lastClassval).val(firstlist.postal_code);
  var domainsListArray = firstlist.domain_ids;
  $('.domain-' + countval + '-' + lastClassval).val(domainsListArray);
  $('.domainselected-' + countval + '-' + lastClassval).val(domainsListArray.length + ' Selected');
  if (firstlist.is_active == true) {
    $('.activedclass-' + countval + '-' + lastClassval).text('Active');
  } else {
    var classnamec = 'imgactivedclass-' + countryByCount + '-' + 1;
    $('.activedclass-' + countval + '-' + lastClassval).html('<img src="/images/icon-inactive.png" onclick="reactiviteunit(this, \'' + firstlist.unit_id + '\', \'' + clientunitId + '\');">');
  }
}
//Submit Record -----------------------------------------------------------------------------------------
$('#btn-clientunit-submit').click(function () {
  clearMessage();
  var clientunitIdValue = $('#client-unit-id').val();
  var groupNameValue = $('#group-select').val();
  var businessgrouptextValue = $('#businessgroup-text').val();
  var businessgroupValue = $('#businessgroup-select').val();
  var businessgroupName = $('#businessgroup-select :selected').text();
  var legalEntityValue = $('#entity-select').val();
  var lentitytextValue = $('#entity-text').val().trim();
  var legalEntityName = $('#entity-select :selected').text();
  var divisiontextValue = $('#division-text').val();
  var divisionValue = $('#division-select').val();
  var divisionName = $('#division-select :selected').text();
  var unitCountValue = $('#unitcount').val();
  var countryVal = $('.country').val();
  if (clientunitIdValue == '') {
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
    if (divisiontextValue == '') {
      divIdValue = parseInt(divisionValue);
      if (divisionValue != '') {
        divNameValue = divisionName;
      } else {
        divNameValue = null;
      }
    } else {
      divIdValue = null;
      divNameValue = divisiontextValue;
    }
    if (bgNameValue != null) {
      businessGroup = mirror.getBusinessGroupDict(bgIdValue, bgNameValue);
    } else {
      businessGroup = null;
    }
    legalEntity = mirror.getLegalEntityDict(leIdValue, leNameValue);
    if (divNameValue != null) {
      division = mirror.getDivisionDict(divIdValue, divNameValue);
    } else {
      division = null;
    }
    var countryWiseUnits = [];
    var numItemsCountry = $('.country').length;
    for (var i = 1; i < numItemsCountry; i++) {
      if ($('.country-' + i).val() != '') {
        var unitarr = [];
        countryUnits = parseInt($('.country-' + i).val());
        var unitcount = $('.no-of-units-' + i).val();
        if (unitcount > 0) {
          var units = [];
          for (var j = 1; j <= unitcount; j++) {
            var unit;
            unitId = null;
            unitCode = $('.unit-code-' + i + '-' + j).val();
            unitName = $('.unit-name-' + i + '-' + j).val().trim();
            unitAddress = $('.unit-address-' + i + '-' + j).val().trim();
            unitPostalCode = $('.postal-code-' + i + '-' + j).val().trim();
            unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
            unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();
            unitIndustryId = $('.industry-' + i + '-' + j).val();
            unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();
            unitdomain = $('.domain-' + i + '-' + j).val();
            if (unitLocation == '' && unitGeographyId == '' && unitCode == '' && unitName == '' && (unitIndustryName == '' || unitIndustryName == 'Select') && unitAddress == '' && unitPostalCode == '' && unitdomain == '') {
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
            } else if (unitIndustryName == '') {
              displayMessage(message.industryname_required);
              return;
            } else if (unitIndustryId == 0) {
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
                var arrayDomainsVal = unitdomain.split(',');
                var arrayDomains = [];
                for (var m = 0; m < arrayDomainsVal.length; m++) {
                  arrayDomains[m] = parseInt(arrayDomainsVal[m]);
                }
                var domainsVal = arrayDomains;
                unit = mirror.getUnitDict(null, unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitLocation, parseInt(unitIndustryId), unitIndustryName, domainsVal);
                units.push(unit);
              } else {
                displayMessage(duplicates + ' Unit Code Already Exits!!!');
                return;
              }
            }
          }
          countryWiseUnits.push(mirror.mapUnitsToCountry(countryUnits, units));
        } else {
          displayMessage(message.add_one_unit);
          return;
        }
      }
    }
    mirror.saveClient(parseInt(groupNameValue), businessGroup, legalEntity, division, countryWiseUnits, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  } else if (clientunitIdValue != '') {
    clearMessage();
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
    var businessgrouptextValue = $('#businessgroup-text').val().trim();
    var businessgroupidupdate = $('#businessgroup-update-id').val();
    var businessgrouptext = $('#businessgroup-select :selected').text().trim();
    var businessgroupid = $('#businessgroup-select').val();
    var lentitytextValue = $('#entity-text').val().trim();
    var legalentityidupdate = $('#legalentity-update-id').val();
    var legalentityid = $('#entity-select').val();
    var legalentitytext = $('#entity-select :selected').text();
    var divisiontextValue = $('#division-text').val().trim();
    var divisionidupdate = $('#division-update-id').val();
    var divisionid = $('#division-select').val();
    var divisiontext = $('#division-select :selected').text();
    if (businessgrouptextValue == '' && businessgroupidupdate != '') {
      displayMessage(message.businessgroup_required);
      return;
    } else if (businessgrouptextValue != '' && businessgroupidupdate != '') {
      businessGroup = mirror.getBusinessGroupDict(parseInt(businessgroupidupdate), businessgrouptextValue);
    } else if (businessgrouptext != '' && businessgroupid != '') {
      businessGroup = mirror.getBusinessGroupDict(parseInt(businessgroupid), businessgrouptext);
    } else {
      businessGroup = null;
    }
    if (lentitytextValue == '' && legalentityidupdate != '') {
      displayMessage(message.legalentity_required);
      return;
    } else if (lentitytextValue != '' && legalentityidupdate != '') {
      legalEntity = mirror.getLegalEntityDict(parseInt(legalentityidupdate), lentitytextValue);
    } else if (legalentityid != '' && legalentitytext != '') {
      legalEntity = mirror.getLegalEntityDict(parseInt(legalentityid), legalentitytext);
    } else {
      legalEntity = mirror.getLegalEntityDict(parseInt(legalentityid), legalentitytext);
    }
    if (divisiontextValue == '' && divisionidupdate != '') {
      displayMessage(message.division_required);
      return;
    } else if (divisiontextValue != '' && divisionidupdate != '') {
      division = mirror.getDivisionDict(parseInt(divisionidupdate), divisiontextValue);
    } else if (divisionid != '' && divisiontext != '') {
      division = mirror.getDivisionDict(parseInt(divisionid), divisiontext);
    } else {
      division = null;
    }
    var countryWiseUnits = [];
    var numItemsCountry = $('.country').length;
    for (var i = 1; i < numItemsCountry; i++) {
      var countryUnits = {};
      var unitarr = [];
      if ($('.country-' + i).val() != '') {
        countryUnits = parseInt($('.country-' + i).val());
        var unitcount = $('.no-of-units-' + i).val();
        var units = [];
        for (var j = 1; j <= unitcount; j++) {
          var unit;
          unitId = $('.unit-id-' + i + '-' + j).val();
          ;
          unitCode = $('.unit-code-' + i + '-' + j).val();
          unitName = $('.unit-name-' + i + '-' + j).val().trim();
          unitAddress = $('.unit-address-' + i + '-' + j).val().trim();
          unitPostalCode = $('.postal-code-' + i + '-' + j).val().trim();
          unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
          unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();
          unitIndustryId = $('.industry-' + i + '-' + j).val();
          unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();
          unitdomain = $('.domain-' + i + '-' + j).val();
          // if(unitLocation == '' && unitGeographyId == '' &&  unitCode == '' &&  unitName == '' &&  unitIndustryId == 'NaN' && unitAddress == '' && unitPostalCode == '' && unitdomain == ''){
          if (unitLocation == '' && unitGeographyId == '' && unitCode == '' && unitName == '' && (unitIndustryName == '' || unitIndustryName == 'Select') && unitAddress == '' && unitPostalCode == '' && unitdomain == '') {
            if (unitcount == 1) {
              displayMessage(message.add_one_unit);
              return;
            }
            continue;
          } else if (unitLocation == '') {
            $('.error-message').show();
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
          } else if (unitIndustryName == '') {
            displayMessage(message.industryname_required);
            return;
          } else if (unitIndustryId == 0) {
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
              var arrayDomainsVal = unitdomain.split(',');
              var arrayDomains = [];
              for (var m = 0; m < arrayDomainsVal.length; m++) {
                arrayDomains[m] = parseInt(arrayDomainsVal[m]);
              }
              var domainsVal = arrayDomains;
              unit = mirror.getUnitDict(parseInt(unitId), unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitLocation, parseInt(unitIndustryId), unitIndustryName, domainsVal);
              units.push(unit);
            } else {
              displayMessage(duplicates + ' Unit Code Already Exists!!!');
              return;
            }
          }
        }
        countryWiseUnits.push(mirror.mapUnitsToCountry(countryUnits, units));
      }
    }
    mirror.updateClient(parseInt(clientunitIdValue), businessGroup, legalEntity, division, countryWiseUnits, function (error, response) {
      if (error == null) {
        onSuccess(response);
        isUpdate = false;
      } else {
        onFailure(error);
      }
    });
  } else {
    console.log('Fails All');
  }
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
function activate_text(element, ccount) {
  var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $('.countryval-' + ccount).val(checkname);
  $('.country-' + ccount).val(checkval);
  $('.glevel-' + checkval).empty();
}
function onArrowKey_Client(e, ac_item, ccount, multipleselect) {
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
      $('.countryval-' + ccount).val(ac_name);
      $('.country-' + ccount).val(ac_id);
      $('.glevel-' + ac_id).empty();
      $('.autocompleteview-' + ccount).css('display', 'none');
    } else {
      $('.unitlocation' + ccount).val(ac_name);
      $('.unitlocation-ids' + ccount).val(ac_id);
      for (var geography in geographyList) {
        var geolist = geographyList[geography];
        for (var glist in geolist) {
          if (geolist[glist].geography_id == parseInt(ac_id)) {
            mappingname = geolist[glist].mapping;
          }
        }
      }
      $('.full-location-list' + ccount).html('<br>' + mappingname);
      $('.auto-complete-unit-location').css('display', 'none');
    }
    return false;
  }
}

function loadauto_countrytext(textval, classval, e) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-').pop();
  $('.autocompleteview ac-' + ccount).css('display', 'block');
  //var a = $(".autocompleteview ac-textbox");
  //alert(a.style.display);

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

  //$('.ulist-text-' + ccount).empty();
  $('.ulist-text').empty();
  if (textval.length > 0) {
    for (var i in countries) {
      for (var j = 0; j < arrayCountry.length; j++) {
        if (arrayCountry[j] == countries[i].country_id) {
          if (~countries[i].country_name.toLowerCase().indexOf(textval.toLowerCase()) && countries[i].is_active == 1)
            suggestions.push([
              countries[i].country_id,
              countries[i].country_name
            ]);
        }
      }
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '" onclick="activate_text(this,' + ccount + ')">' + suggestions[i][1] + '</li>';
    }
    alert(str);
    //$('.ulist-text-' + ccount).append(str);
    $('.ulist-text').append(str);
    $('.country-' + ccount).val('');
  }
  onArrowKey_Client(e, 'autocompleteview-' + ccount, ccount, 'country');
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
    for (var geography in geographyList) {
      var geolist = geographyList[geography];
      for (var glist in geolist) {
        if (geolist[glist].level_id == glevelval) {
          if (~geolist[glist].geography_name.toLowerCase().indexOf(textval.toLowerCase()) && geolist[glist].is_active == 1)
            suggestions.push([
              geolist[glist].geography_id,
              geolist[glist].geography_name,
              geolist[glist].mapping
            ]);
        }
      }
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '" onclick="activate_unitlocaion(this,\'' + countval + '\', \'' + suggestions[i][2].replace(/"/gi, '##') + '\')">' + suggestions[i][1] + '</li>';
    }
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
//Load Domain  for Unit
function loaddomain(classval) {
  var lastClass = classval.split(' ').pop();
  var ccount = lastClass.split('-');
  var countval = '-' + ccount[1] + '-' + ccount[2];
  $('.domain-selectbox-view' + countval).css('display', 'block');
  var getClientid;
  if ($('#client-unit-id').val() == '') {
    getClientid = $('#group-select').val();
  } else {
    getClientid = $('#client-unit-id').val();
  }
  var clientdomainsid;
  $.each(groupList, function (key, val) {
    if (val.client_id == getClientid) {
      clientdomainsid = val.domain_ids;
    }
  });
  var editdomainval = [];
  if ($('.domain' + countval).val() != '') {
    editdomainval = $('.domain' + countval).val().split(',');
  }
  if ($('#client-unit-id').val() == '') {
    var domains = domainList;
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
      if (checkdomainforadd(clientdomainsid, domainId) == 1) {
        if (selectdomainstatus == 'checked') {
          str += '<li id="' + domainId + '" class="active_selectbox' + countval + ' active" onclick="activate(this,\'' + countval + '\' )" >' + domainName + '</li> ';
        } else {
          str += '<li id="' + domainId + '" onclick="activate(this,\'' + countval + '\')" >' + domainName + '</li> ';
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
            str += '<li id = "' + domainId + '" class="active_selectbox' + countval + ' active" onclick="activate(this, \'' + countval + '\')" >' + domainName + '</li> ';
          } else {
            str += '<li id="' + domainId + '" onclick="activate(this, \'' + countval + '\')" >' + domainName + '</li> ';
          }
        } else if (ccdd != 1 && cdd == 1) {
          str += '<li id="' + domainId + '" onclick="activate(this, \'' + countval + '\')" >' + domainName + '</li> ';
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
    if (chkstatus == 'active_selectbox' + count + ' active') {
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active_selectbox' + count);
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active');
    } else {
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active_selectbox' + count);
      $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active');
    }
    activate_domain(count);
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
//check & uncheck process
function activate(element, count) {
  var chkstatus = $(element).attr('class');
  if (chkstatus == 'active_selectbox' + count + ' active') {
    $(element).removeClass('active_selectbox' + count);
    $(element).removeClass('active');
  } else {
    $(element).addClass('active_selectbox' + count);
    $(element).addClass('active');
  }
  activate_domain(count);
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
