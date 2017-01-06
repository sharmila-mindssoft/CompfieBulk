var statutoryMappingDataList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoriesList;
var complianceFrequencyList;
var temp_act = null;
var finalList;
var count = 1;
var compliance_count = 0;
var lastActName = '';
var lastOccuranceid = 0;
var s_endCount = 0;
var totalRecord;
var filterdata = {};
var mappedStatutory;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACOrgtype = $('#ac-industry');
var ACDomain = $('#ac-domain');
var ACStatNature = $('#ac-statutorynature');
var ACGeography = $('#ac-geography');
var ACStatutory = $('#ac-statutory');

//Input field variable declaration
var CountryVal = $('#countryval');
var Country = $('#country');
var OrgtypeVal = $('#industryval');
var Orgtype = $('#industry');
var DomainVal = $('#domainval');
var Domain = $('#domain');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var StatutoryNatureVal = $('#statutorynatureval');
var StatutoryNature = $('#statutorynature');
var GeographyVal = $('#geographyval');
var Geography = $('#geography');
var StatutoryVal = $('#statutoryval');
var Statutory = $('#statutory');

var SubmitButton = $('#submit');
var ExportButton = $('#export');
function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
//get statutory mapping filter details from api
function getStatutoryMappings() {
  function onSuccess(data) {
    industriesList = data.industries;
    statutoriesList = data.level_one_statutories;
    countriesList = data.countries;
    domainsList = data.domains;
    statutoryNaturesList = data.statutory_natures;
    geographiesList = data.geographies;
    complianceFrequencyList = data.compliance_frequency;
    //load compliance frequency selectbox
    for (var compliancefrequency in complianceFrequencyList) {
      var option = $('<option></option>');
      option.val(complianceFrequencyList[compliancefrequency].frequency_id);
      option.text(complianceFrequencyList[compliancefrequency].frequency);
      $('#compliance_frequency').append(option);
    }
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getStatutoryMappingsReportFilter(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
//display statutory mapping details accoring to count
function loadCountwiseResult(filterList) {
  if (compliance_count <= 0) {
    $('.grid-table-rpt').show();
    var country = $('#countryval').val();
    var domain = $('#domainval').val();
    var compliance_frequency = $('#compliance_frequency').val();
    $('.country').text(country);
    $('.domain').text(domain);
    $('.tbody-compliance').find('tbody').remove();
    count = 1;
    compliance_count = 0;
    lastActName = '';
    lastOccuranceid = 0;
  }
  for (var entity in filterList) {
    var actname = filterList[entity].act_name;
    var frequency_id = filterList[entity].frequency_id;
    var industry_names = filterList[entity].industry_names;
    var statutory_nature_name = filterList[entity].statutory_nature_name;
    var statutory_provision = filterList[entity].s_pro_map;
    var compliance_name = filterList[entity].c_task;
    var download_url = filterList[entity].url;
    if (actname != lastActName) {
      var tableRow = $('#act-templates .table-act-list .table-row-act-list');
      var clone = tableRow.clone();
      $('.actname', clone).text(actname);
      $('.tbody-compliance').append(clone);
      
      lastOccuranceid = 0;
      count++;
      
    }
    var occurance = '';
    var occuranceid;
    if (frequency_id != lastOccuranceid) {
      $.each(complianceFrequencyList, function (index, value) {
        if (value.frequency_id == frequency_id) {
          occurance = value.frequency;
          occuranceid = value.frequency_id;
        }
      });
      var tableRow2 = $('#head-templates .table-compliance-frequency-list .table-row-com-frequency');
      var clone2 = tableRow2.clone();
      $('.tbl_heading', clone2).text(occurance);
      $('.tbody-compliance').append(clone2);
    }
    var tableRow1 = $('#compliance-templates .table-compliances-list .table-row');
    var clone1 = tableRow1.clone();
    $('.tbody-compliance').append(clone1);
    $('.tbl_sno', clone1).text(compliance_count + 1);
    $('.tbl_industrytype', clone1).text(industry_names);
    $('.tbl_statutorynature', clone1).text(statutory_nature_name);
    $('.tbl_statutoryprovision', clone1).text(statutory_provision);
    if (download_url == null) {
      $('.tbl_compliancetask', clone1).html(compliance_name);
    } else {
      $('.tbl_compliancetask', clone1).html('<a href= "' + download_url + '" target="_blank" download>' + compliance_name + '</a>');
    }
    var sdateDesc = '';
    var duration = filterList[entity].duration;
    var duration_type_id = filterList[entity].d_type_id;
    var repeats_every = filterList[entity].r_every;
    var repeats_type_id = filterList[entity].r_type_id;
    var statutory_date = filterList[entity].statu_dates;
    var statutorydate = '';
    var duration_type = '';
    var repeats_type = '';
    if (frequency_id == 4) {
      if (duration_type_id == 1) {
        duration_type = 'Day(s)';
      } else {
        duration_type = 'Hour(s)';
      }
      sdateDesc = 'To complete with in ' + duration + ' ' + duration_type;
    } else if (frequency_id == 1) {
      sdateDesc = '';
    } else {
      if (repeats_type_id == 1) {
        repeats_type = 'Day(s)';
      } else if (repeats_type_id == 2) {
        repeats_type = 'Month(s)';
      } else {
        repeats_type = 'Year(s)';
      }
      sdateDesc = 'Every ' + repeats_every + ' ' + repeats_type;
    }
    if (frequency_id != 4) {
      for (z = 0; z < statutory_date.length; z++) {
        var sDay = '';
        if (statutory_date[z].statutory_date != null)
          sDay = statutory_date[z].statutory_date;
        var sMonth = '';
        if (statutory_date[z].statutory_month != null)
          sMonth = statutory_date[z].statutory_month;
        if (sMonth != '')
          sMonth = getMonth_IntegertoString(sMonth);
        statutorydate += sMonth + ' ' + sDay + ' ';
        if (statutorydate.trim() != '')
          statutorydate += ', ';
      }
      if (statutorydate.trim() != '') {
        statutorydate = statutorydate.replace(/,\s*$/, '');
        if (sdateDesc == '') {
          statutorydate = statutorydate;
        } else {
          statutorydate = sdateDesc + ' ( ' + statutorydate + ' )';
        }
      } else {
        statutorydate = sdateDesc;
      }
    } else {
      statutorydate = sdateDesc;
    }
    $('.tbl_description', clone1).text(filterList[entity].description);
    $('.tbl_penalconsequences', clone1).text(filterList[entity].p_consequences);
    $('.tbl_occurance', clone1).text(statutorydate);
    var applicableLocation = '';
    for (var i = 0; i < filterList[entity].geo_maps.length; i++) {
      applicableLocation = applicableLocation + filterList[entity].geo_maps[i] + '<br>';
    }
    $('.tbl_applicablelocation', clone1).html(applicableLocation);
    $('.tbody-compliance').append(clone1);
    compliance_count = compliance_count + 1;
    lastActName = actname;
    lastOccuranceid = frequency_id;
  }
  if (compliance_count > 0) {
    $('.compliance_count').text('Showing ' + 1 + ' to ' + compliance_count + ' of ' + totalRecord);
  } else {
    $('.compliance_count').text('');
  }

  if (compliance_count >= totalRecord) {
    //$('#pagination').hide();
  }
  if (count == 1) {
    var tableRow1 = $('#nocompliance-templates .table-nocompliances-list .table-row');
    var clone1 = tableRow1.clone();
    $('.tbody-compliance').append(clone1);
    $('.tbl_norecords', clone1).text('No Records');
    $('.tbody-compliance').append(clone1);
    //$('#pagination').hide();
  }
}
function loadresult() {
  /*var c_frequency = $("#compliance_frequency").val();
  if(c_frequency == 'All'){
    finalList = statutoryMappingDataList;
  }else{
    var filteredList=[];
    for(var entity in statutoryMappingDataList) {
      var filter_frequency = statutoryMappingDataList[entity]["frequency_id"];
      if (c_frequency == filter_frequency) filteredList.push(statutoryMappingDataList[entity]);
    }
    finalList = filteredList;
  }*/
  loadCountwiseResult(statutoryMappingDataList);
}
$('#pagination').click(function () {
  s_endCount = compliance_count;
  filterdata.r_count = parseInt(s_endCount);
  displayLoader();
  function onSuccess(data) {
    statutoryMappingDataList = data.statutory_mappings;
    totalRecord = data.total_count;
    loadresult();
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
    hideLoader();
  }
  mirror.getStatutoryMappingsReportData(filterdata, function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
});
// get statutory mapping report data from api
$('#submit').click(function () {
  $('#pagination').show();
  var country = $('#country').val();
  var domain = $('#domain').val();
  var industry = null;
  var statutorynature = null;
  var geography = null;
  var act = null;
  var c_frequency = null;
  if ($('#industry').val() != '')
    industry = $('#industry').val();
  if ($('#statutorynature').val() != '')
    statutorynature = $('#statutorynature').val();
  if ($('#geography').val() != '')
    geography = $('#geography').val();
  if ($('#statutory').val() != '')
    act = $('#statutory').val();
  if ($('#compliance_frequency').val() != '')
    c_frequency = $('#compliance_frequency').val();
  if (country.length == 0) {
    displayMessage(message.country_required);
  } else if (domain.length == 0) {
    displayMessage(message.domain_required);
  } else {
    count = 1;
    compliance_count = 0;
    lastActName = '';
    lastOccuranceid = 0;
    displayLoader();

    s_endCount = 0;
    filterdata = {};
    filterdata.c_id = parseInt(country);
    filterdata.d_id = parseInt(domain);
    filterdata.a_i_id = parseInt(industry);
    filterdata.a_s_n_id = parseInt(statutorynature);
    filterdata.a_g_id = parseInt(geography);
    filterdata.statutory_id_optional = parseInt(act);
    filterdata.frequency_id = parseInt(c_frequency);
    filterdata.r_count = parseInt(s_endCount);
    function onSuccess(data) {
      statutoryMappingDataList = data.statutory_mappings;
      totalRecord = data.total_count;
      loadresult();
      hideLoader();
    }
    function onFailure(error) {
      displayMessage(error);
      hideLoader();
    }
    mirror.getStatutoryMappingsReportData(filterdata, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
    temp_act = act;
  }
});

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    var current_id = id_element[0].id;
    if(current_id == 'country'){
      DomainVal.val('');
      Domain.val('');
      OrgtypeVal.val('');
      Orgtype.val('');
      StatutoryNatureVal.val('');
      StatutoryNature.val('');
      GeographyVal.val('');
      Geography.val('');
      StatutoryVal.val('');
      Statutory.val('');
    }else if(current_id == 'domain'){
      OrgtypeVal.val('');
      Orgtype.val('');
      StatutoryNatureVal.val('');
      StatutoryNature.val('');
      GeographyVal.val('');
      Geography.val('');
      StatutoryVal.val('');
      Statutory.val('');
    }else if(current_id == 'industry'){
      StatutoryNatureVal.val('');
      StatutoryNature.val('');
      GeographyVal.val('');
      Geography.val('');
      StatutoryVal.val('');
      Statutory.val('');
    }else if(current_id == 'statutorynature'){
      GeographyVal.val('');
      Geography.val('');
      StatutoryVal.val('');
      Statutory.val('');
    }else if(current_id == 'geography'){
      StatutoryVal.val('');
      Statutory.val('');
    }
}

//Autocomplete Script Starts
//retrive country autocomplete value
//load country list in autocomplete text box
CountryVal.keyup(function(e){
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACCountry, Country, text_val,
    countriesList, "country_name", "country_id", function (val) {
      onAutoCompleteSuccess(CountryVal, Country, val);
    });
});

//load domain list in autocomplete textbox
DomainVal.keyup(function(e){
  var condition_fields = [];
  var condition_values = [];
  if(Country.val() != ''){
    condition_fields.push("country_ids");
    condition_values.push(Country.val());
  }
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACDomain, Domain, text_val,
    domainsList, "domain_name", "domain_id", function (val) {
        onAutoCompleteSuccess(DomainVal, Domain, val);
    }, condition_fields, condition_values);
});

//load industry list in autocomplete textbox
$('#industryval').keyup(function (e) {
  var condition_fields = [];
  var condition_values = [];
  if(Country.val() != '' && Domain.val() != ''){
    condition_fields.push("country_ids");
    condition_values.push(Country.val());
    condition_fields.push("domain_id");
    condition_values.push(Domain.val());
  }
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACOrgtype, Orgtype, text_val,
    industriesList, "industry_name", "industry_id", function (val) {
      onAutoCompleteSuccess(OrgtypeVal, Orgtype, val);
    }, condition_fields, condition_values);
});

//load statutorynature list in autocomplete textbox
$('#statutorynatureval').keyup(function (e) {
  var textval = $(this).val();
  var condition_fields = [];
  var condition_values = [];
  if(Country.val() != ''){
    condition_fields.push("country_ids");
    condition_values.push(Country.val());
  }
  commonAutoComplete(
    e, ACStatNature, StatutoryNature, textval,
    statutoryNaturesList, "statutory_nature_name", "statutory_nature_id", function (val) {
      onAutoCompleteSuccess(StatutoryNatureVal, StatutoryNature, val);
    }, condition_fields, condition_values);
});

//load geography list in autocomplete textbox
$('#geographyval').keyup(function (e) {
  var textval = $(this).val();
  if(Country.val() != ''){
  commonAutoComplete(
    e, ACGeography, Geography, textval,
    geographiesList[$('#country').val()], "geography_name", "geography_id", function (val) {
      onAutoCompleteSuccess(GeographyVal, Geography, val);
    });
  }
});

//load statutory list in autocomplete textbox
$('#statutoryval').keyup(function (e) {
  var textval = $(this).val();
  var condition_fields = [];
  var condition_values = [];
  if(Country.val() != '' && Domain.val() != ''){
    condition_fields.push("country_id");
    condition_values.push(Country.val());
    condition_fields.push("domain_id");
    condition_values.push(Domain.val());

    commonAutoComplete(
    e, ACStatutory, Statutory, textval,
    //statutoriesList[$('#country').val()][$('#domain').val()], "statutory_name", "statutory_id", function (val) {
    statutoriesList, "level_1_statutory_name", "level_1_statutory_id", function (val) {
      onAutoCompleteSuccess(StatutoryVal, Statutory, val);
    }, condition_fields, condition_values);
  }
});
//Autocomplete Script ends
//initialization
$(function () {
  $('.grid-table-rpt').hide();
  getStatutoryMappings();
  $('#countryval').focus();
});
