var riskComplianceList;
var countriesList;
var domainsList;
var businessGroupsList;
var legalEntitiesList;
var divisionsList;
var unitsList;
var actList;

var on_current_page = 1;
var totalRecord;
var sno = 0;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
//get risk report filters from api
function getRiskReportFilters() {
  function onSuccess(data) {
    countriesList = data.countries;
    domainsList = data.domains;
    businessGroupsList = data.business_groups;
    legalEntitiesList = data.legal_entities;
    divisionsList = data.divisions;
    unitsList = data.units;
    actList = data.level1_statutories;
    loadCountries(countriesList);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  client_mirror.getRiskReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

function getValue(field_name){
   if (field_name == "country") {
        c_id = $('#country').val().trim();
        if (c_id == '') {
            return null;
        }
        return parseInt(c_id);
    }
    else if (field_name == "domain") {
        d_id = $('#domain').val().trim();
        if (d_id == '') {
            return null;
        }
        return parseInt(d_id);
    }
    else if (field_name == "bg") {
        bg_id = $('#businessgroup').val().trim();
        if (bg_id == '') {
            return null;
        }
        return parseInt(bg_id);;
    }
    else if (field_name == "le") {
        le_id = $('#legalentity').val().trim();
        if (le_id == '') {
            return null;
        }
        return parseInt(le_id);
    }
    else if (field_name == "division") {
        dv_id = $('#division').val().trim();
        if (dv_id == '') {
            return null;
        }
        return parseInt(dv_id);
    }
    else if (field_name == "unit") {
        u_id = $('#unit').val().trim();
        if (u_id == '') {
            return null;
        }
        return parseInt(u_id);
    }
    else if (field_name == "act") {
        act = $('#act').val().trim();
        if (act == '') {
            return null;
        }
        return act;
    }
    else if (field_name == "status") {
        status = $('#statutory_status').val().trim();
        if (status == '') {
            return null;
        }
        return parseInt(status);
    }
};

function validateMandatory(){
    is_valid = true;
    if (getValue("country") == null) {
        displayMessage(message.country_required);
        is_valid = false;
    }
    else if (getValue("domain") == null) {
        displayMessage(message.domain_required);
        is_valid = false;
    }
    return is_valid;
};

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
function hidePagePan() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

//load report data
function loadCompliances(complianceList) {
  $('.tbody-unit').find('tbody').remove();
  var showFrom = sno + 1;
  var is_null = true;

  var country = $('#country').find('option:selected').text();
  var domain = $('#domainval').val();
  
  for (var entity in complianceList) {
    var bg = '-';
    if (complianceList[entity].business_group_name != null)
      bg = complianceList[entity].business_group_name;
    var dv = '-';
    if (complianceList[entity].division_name != null)
      dv = complianceList[entity].division_name;
    var le = complianceList[entity].legal_entity_name;

    var tableRow = $('#unit-list-templates .table-unit-list .table-row-unit-list');
    var clone = tableRow.clone();
    $('.tbl_country', clone).text(country);
    $('.tbl_domain', clone).text(domain);
    $('.tbl_businessgroup', clone).text(bg);
    $('.tbl_division', clone).text(dv);
    $('.tbl_legalentity', clone).text(le);
    $('.tbody-unit').append(clone);
      
    var statutoryUnits = complianceList[entity].level_1_statutory_wise_units;
    for (var statutoryUnit in statutoryUnits) {
      var tableRow5 = $('#unit-head-templates .table-unit-head .table-row-act-name');
      var clone5 = tableRow5.clone();
      $('.tbl_actname', clone5).html('<div class="heading" style="margin-top:5px;width:auto;">' + statutoryUnit + '</div>');
      $('.tbody-unit').append(clone5);
      var tableRow1 = $('#unit-head-templates .table-unit-head .table-row-unit-head');
      var clone1 = tableRow1.clone();
      $('.tbody-unit').append(clone1);
        
      for (var j = 0; j < statutoryUnits[statutoryUnit].length; j++) {
        var uName = statutoryUnits[statutoryUnit][j].unit_name;
        var uAddress = statutoryUnits[statutoryUnit][j].address;
        var tableRow2 = $('#unit-name-templates .table-unit-name .table-row-unit-name');
        var clone2 = tableRow2.clone();
        $('.tbl_unitheading', clone2).html('<abbr class="page-load tipso_style" title="' + uAddress + '"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>' + uName);
        $('.tbody-unit').append(clone2);
          
        var uCompliences = statutoryUnits[statutoryUnit][j].compliances;
        for (i = 0; i < uCompliences.length; i++) {
          is_null = false;
          sno++;
          var tableRow3 = $('#unit-content-templates .table-unit-content .table-row-unit-content');
          var clone3 = tableRow3.clone();
          var pc = '';
          if (uCompliences[i].penal_consequences != null) {
            pc = uCompliences[i].penal_consequences;
          }
          $('.tbl_sno', clone3).text(sno);
          $('.tbl_statutoryprovision', clone3).text(uCompliences[i].statutory_mapping);
          $('.tbl_compliance', clone3).text(uCompliences[i].compliance_name);
          $('.tbl_description', clone3).text(uCompliences[i].description);
          $('.tbl_penalconsequences', clone3).text(pc);
          $('.tbl_frequency', clone3).text(uCompliences[i].compliance_frequency);
          $('.tbl_repeats', clone3).text(uCompliences[i].repeats);
          $('.tbody-unit').append(clone3);
        }
      }
    }
  }
  hideLoader();
  if (is_null == true) {
    hidePagePan();
  }
  else {
    showPagePan(showFrom, sno, totalRecord);
  }
}


function createPageView(total_records) {
    perPage = parseInt($('#items_per_page').val());
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                fetchData(false);
            }
        }
    });
};

function fetchData (csv) {
    displayLoader();
    _country = getValue("country");
    _domain = getValue("domain");
    _le = getValue("le");
    _bg = getValue("bg");
    _division = getValue("division");
    _unit = getValue("unit");
    _act = getValue("act");
    _status = getValue("status");
    _page_limit = parseInt($('#items_per_page').val());

    if (on_current_page == 1) {
      sno = 0
    }
    else {
      sno = (on_current_page - 1) *  _page_limit;
    }

    client_mirror.getRiskReport(_country, _domain, _bg, _le, 
    _division, _unit, _act, _status, csv, sno, _page_limit,
        function(error, response) {
            if (error != null) {
                displayMessage(error);
            }
            else {

              if (csv) {
                var download_url = response.link;
                window.open(download_url, '_blank'); 
                hideLoader();
              }else{
                sno  = sno;
                riskComplianceList = response.compliance_list;
                totalRecord = response.total_record;

                if (totalRecord == 0) {
                  $('.tbody-unit').find('tbody').remove();
                  var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
                  var clone4 = tableRow4.clone();
                  $('.no_records', clone4).text('No Compliance Found');
                  $('.tbody-unit').append(clone4);
                  $('.pagination-view').hide();
                  hideLoader();
                } else {
                  if(sno==0){
                    createPageView(totalRecord);
                  }
                  $('.pagination-view').show();
                  loadCompliances(riskComplianceList);
                  
                }
              }

            }
        }
    );
};

$('#items_per_page').on('change', function (e) {
  perPage = parseInt($(this).val());
  sno = 0;
  on_current_page = 1;
  createPageView(totalRecord);
  fetchData(false);
});

function loadCompliance(csv){
  is_valid = validateMandatory();
  if (is_valid == true) {
    $('.grid-table-rpt').show();
    fetchData(csv);
  }
}

$('#submit').click(function () {
  loadCompliance(false);
});
$('#export').click(function () {
  loadCompliance(true);
});


/*//get risk report data from api
function loadCompliance(reportType) {
  displayLoader();
  var country = $('#country').val();
  var domain = $('#domain').val();
  var businessgroup = null;
  var legalentity = null;
  var division = null;
  var unit = null;
  var act = null;
  var statutory_status = null;
  if ($('#businessgroup').val() != '')
    businessgroup = $('#businessgroup').val();
  if ($('#legalentity').val() != '')
    legalentity = $('#legalentity').val();
  if ($('#division').val() != '')
    division = $('#division').val();
  if ($('#unit').val() != '')
    unit = $('#unit').val();
  if ($('#act').val() != '')
    act = $('#act').val().trim();
  statutory_status = $('#statutory_status').val();
  if (country.length == 0) {
    displayMessage(message.country_required);
    $('.grid-table-rpt').hide();
    hideLoader();
    return false;
  } else if (domain.length == 0) {
    displayMessage(message.domain_required);
    $('.grid-table-rpt').hide();
    hideLoader();
    return false;
  } else {
    $('.grid-table-rpt').show();
    clearMessage();
    function onSuccess(data) {
      riskComplianceList = data.compliance_list;
      totalRecord = data.total_record;
      loadresult(riskComplianceList);
      hideLoader();
      if (reportType == 'export') {
        var download_url = data.link;
        window.open(download_url, '_blank');
      }
    }
    function onFailure(error) {
      displayMessage(error);
      hideLoader();
    }
    var csv = true;
    if (reportType == 'show') {
      csv = false;
    }
    client_mirror.getRiskReport(parseInt(country), parseInt(domain), parseInt(businessgroup), parseInt(legalentity), parseInt(division), parseInt(unit), act, parseInt(statutory_status), csv, sno, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
}
//pagination process
$('#pagination').click(function () {
  loadCompliance('show');
});
$('#submit').click(function () {
  sno = 0;
  lastBG = '';
  lastDv = '';
  lastLE = '';
  lastUnit = '';
  lastAct = '';
  $('.tbody-unit').find('tbody').remove();
  loadCompliance('show');
});
$('#export').click(function () {
  loadCompliance('export');
});*/
//Autocomplete Script Starts
//load country list
function loadCountries(countriesList) {
  $('#country').append($('<option value=""> Select </option>'));
  $.each(countriesList, function (key, values) {
    var countryId = countriesList[key].country_id;
    var countryName = countriesList[key].country_name;
    if (countriesList[key].is_active)
      $('#country').append($('<option value="' + countryId + '">' + countryName + '</option>'));
  });
}
//retrive domain autocomplete value
function onDomainSuccess(val) {
  $('#domainval').val(val[1]);
  $('#domain').val(val[0]);
  $('#domainval').focus();
}
//load domain list in autocomplete textbox  
$('#domainval').keyup(function (e) {
  function callback(val) {
    onDomainSuccess(val);
  }
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, domainsList, callback, flag = true);
});
//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val) {
  $('#businessgroupval').val(val[1]);
  $('#businessgroup').val(val[0]);
  $('#businessgroupval').focus();
}
//load businessgroup form list in autocomplete text box  
$('#businessgroupval').keyup(function (e) {
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(e, textval, businessGroupsList, function (val) {
    onBusinessGroupSuccess(val);
  });
});
//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val) {
  $('#legalentityval').val(val[1]);
  $('#legalentity').val(val[0]);
  $('#legalentityval').focus();
}
//load legalentity form list in autocomplete text box  
$('#legalentityval').keyup(function (e) {
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(e, textval, legalEntitiesList, function (val) {
    onLegalEntitySuccess(val);
  });
});
//retrive division form autocomplete value
function onDivisionSuccess(val) {
  $('#divisionval').val(val[1]);
  $('#division').val(val[0]);
  $('#divisionval').focus();
}
//load division form list in autocomplete text box  
$('#divisionval').keyup(function (e) {
  var textval = $(this).val();
  getClientDivisionAutocomplete(e, textval, divisionsList, function (val) {
    onDivisionSuccess(val);
  });
});
//retrive unit form autocomplete value
function onUnitSuccess(val) {
  $('#unitval').val(val[1]);
  $('#unit').val(val[0]);
  $('#unitval').focus();
}
//load unit  form list in autocomplete text box  
$('#unitval').keyup(function (e) {
  var textval = $(this).val();
  //var cId = $("#country").val();
  //var dId = $("#domain").val();
  getUnitAutocomplete(e, textval, unitsList, function (val) {
    onUnitSuccess(val);
  });
});
//retrive statutory autocomplete value
function onStatutorySuccess(val) {
  $('#actval').val(val[1]);
  $('#act').val(val[0].replace(/##/gi, '"'));
  $('#actval').focus();
}
//load statutory list in autocomplete textbox  
$('#actval').keyup(function (e) {
  var textval = $(this).val();
  getClientStatutoryAutocomplete(e, textval, actList, function (val) {
    onStatutorySuccess(val);
  });
});
//Autocomplete Script ends
//initialization
$(function () {
  $('.grid-table-rpt').hide();
  getRiskReportFilters();
  $('#country').focus();
  loadItemsPerPage();
});