var CHART_FILTERS_DATA = null;
var COUNTRIES = {};
var DOMAINS = {};
var BUSINESS_GROUPS = {};
var LEGAL_ENTITIES = {};
var DIVISIONS = {};
var CATEGORIES = {};
var UNITS = {};
var DOMAIN_INFO = {};
var GROUP_NAME = null;
var COMPLIANCE_STATUS_DATA;
var COMPLIANCE_STATUS_DRILL_DOWN_DATE = null;
var ESCALATION_DATA = null;
var ESCALATION_STATUS_DRILL_DOWN_DATA = null;
var TREND_CHART_DATA = null;
var NOT_COMPLIED_DATA = null;
var NOT_COMPLIED_DRILL_DOWN_DATA = null;
var COMPLIANCE_APPLICABILITY_DATA = null;
var COMPLIANCE_APPLICABILITY_DRILL_DOWN = null;
var COUNTRYLIST = null;
var BUSINESSGROUPSLIST = null;
var LEGALENTITYLIST = null;
var DIVISIONLIST = null;
var CATEGORYLIST = null;
var USERLIST = null;
var UNITLIST = null;
var DOMAINLIST = null;
var PAGESIZE = 500;
var STARTCOUNT = 0;
var ENDCOUNT;
var SNO = 0;
var FULLARRAYLIST = [];
var ACCORDIONCOUNT = 0;
var ACCORDIONCOUNTNC = 0;
var ACCORDIONCOUNTD = 0;
var RECORDCOUNT = 0;
var snoAssignee = 0;
var totalRecordAssignee;
var lastAct = '';
var lastStatus = '';
var CS_STATUS = null;
var CS_FILTERTYPEID = null;
var CS_FILTERTYPENAME = null;
var CS_LAST_UNITNAME = null;
var CS_LAST_LEVEL1 = null;
var ES_YEAR = null;
var ES_STATUS = null;
var ES_STATUS1 = null;
var ES_NC_UNITNAME = null;
var ES_NC_LEVEL1 = null;
var ES_NC_COUNT = 1;
var ES_D_UNITNAME = null;
var ES_D_LEVEL1 = null;
var ES_D_COUNT = 1;
var NC_TYPE = null;
var NC_UNITNAME = null;
var NC_LEVEL1 = null;
var TC_YEAR = null;
var TC_UNIT = null;
var TC_LEVEL1 = null;
var CAS_TYPE = null;
var CAS_LEVEL1 = null;
var CAS_UNITNAME = null;

var PageTitle = $('.page-title');
// Assignee wise compliance (AWC) Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACDivision = $('#ac-division');
var ACUnit = $('#ac-unit');
var ACUser = $('#ac-user');

// AWC Input field variable declaration
var CountryVal = $('#awc-country');
var Country = $('#awc-country-id');
var BusinessGroupVal = $('#awc-businessgroup');
var BusinessGroup = $('#awc-businessgroup-id');
var LegalEntityVal = $('#awc-legalentity');
var LegalEntity = $('#awc-legalentity-id');
var DivisionVal = $('#awc-division');
var Division = $('#awc-division-id');
var UnitVal = $('#awc-unit');
var Unit = $('#awc-unit-id');
var UserVal = $('#awc-user');
var User = $('#awc-user-id');

var chartInput = new ChartInput();

//  Compliance Status Chart
function updateComplianceStatusChart(data_input) {
  var data = prepareComplianceStatusChartData(data_input);
  if (data == null)
    return;
  chartType = getFilterTypeTitle();
  if (chartType == 'Consolidated') {
    chartTitle = 'Consolidated Chart';
    updateComplianceStatusPieChart(data, chartTitle, 'pie', null);
    hideButtons();
  } else {
    $('.div-drilldown-container').hide();
    $('.chart-container').show();
    $('.graph-selections-bottom').show();
    $('.div-assignee-wise-compliance').hide();
    currentYear = chartInput.getCurrentYear();
    chartYear = chartInput.getChartYear();
    range = chartInput.getRangeIndex();
    if (chartYear == 0 || chartYear == currentYear) {
      $('.btn-next-year').hide();
    } else {
      $('.btn-next-year').show();
    }
    if (currentYear - 7 == chartYear) {
      $('.btn-previous-year').hide();
    } else {
      $('.btn-previous-year').show();
    }
    $('.btn-back').on('click', function () {
      updateComplianceStatusStackBarChart(data);
      hideButtons();
    });
    updateComplianceStatusStackBarChart(data);
  }
}
function complianceDrillDown(data_list, chartTitle, filter_name) {
  $('.btn-bar-chart').on('click', function () {
    updateComplianceStatusPieChart(data_list, chartTitle, 'column', filter_name);
  });
  $('.btn-pie-chart').on('click', function () {
    updateComplianceStatusPieChart(data_list, chartTitle, 'pie', filter_name);
  });
}
function updateDrillDown(status, data, filterTypeName) {
  console.log("Enter updateDrillDown");
  $('.chart-container').hide();
  $('.graph-selections-bottom').hide();
  $('.div-drilldown-container').show();
  $('.drilldown-container').empty();
  $('.btn-back').show();
  $('.div-assignee-wise-compliance').hide();
  showDrillDownRecord(status, data, filterTypeName);
}
function updateEscalationDrillDown(data, year) {
  $('.chart-container').hide();
  $('.div-drilldown-container').show();
  $('.drilldown-container').show();
  $('.btn-back').show();
  $('.div-assignee-wise-compliance').hide();
  $('.drilldown-container').empty();
  showEscalationDrillDownRecord(data, year);
}
function updateNotCompliedDrillDown(status, data) {
  $('.chart-container').hide();
  $('.graph-selections-bottom').hide();
  $('.div-drilldown-container').show();
  $('.drilldown-container').show();
  $('.assignee-wise').hide();
  $('.btn-back').show();
  showNotCompliedDrillDownRecord(data);
}
function updateComplianceApplicabilityDrillDown(status, data, type) {
  $('.chart-container').hide();
  $('.graph-selections-bottom').hide();
  $('.div-drilldown-container').show();
  $('.drilldown-container').show();
  $('.btn-back').show();
  $('.div-assignee-wise-compliance').hide();
  showComplianceApplicabilityDrillDownRecord_set(data, type);
}
function showComplianceApplicabilityDrillDownRecord_set(data, type) {
  $('.level-heading').attr('colspan', '7');
  $('.page-title').text(GROUP_NAME + ' - ' + type + ' Compliances');  
  $('.drilldown-container').empty();
  $('.div-assignee-wise-compliance').hide();
  $('.escalation-drilldown-container').empty();
  showComplianceApplicabilityDrillDownRecord_headingList();
  showComplianceApplicabilityDrillDownRecord(data, type);
}
function showmorerecords() {
  var getcharttype = chartInput.chart_type;
  // Possiblities: "compliance_status", "escalations", "not_complied", "compliance_report", "trend_chart", "applicability_status"
  if (getcharttype == 'compliance_status') {
    year = chartInput.getChartYear();
    if (year == 0) {
      year = chartInput.getCurrentYear();
    }
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace('_', '-');
    filterType = hyphenatedToUpperCamelCase(filterType);    
    requestData = {
      'd_ids': chartInput.getDomains(),
      'from_date': chartInput.getFromDate(),
      'to_date': chartInput.getToDate(),
      'filter_type': CS_FILTERTYPENAME,
      'filter_id': CS_FILTERTYPEID,
      'compliance_status': CS_STATUS,
      'chart_year': year,
      'record_count': SNO,
      'le_ids': chartInput.getLegalEntities()
    };
    client_mirror.getComplianceStatusDrillDown(requestData, function (status, data) {
      complianceStatusDrilldown(CS_STATUS, data.drill_down_data);
    });
  } else if (getcharttype == 'escalations') {
    ES_YEAR = chartInput.getEscalationYearDrilldown();
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace('_', '-');
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == 'Group') {
      filter_ids = chartInput.getCountries();
    } else {
      filter_ids = getFilterIds(filter_type);
    }
    var requestData = {
      'd_ids': chartInput.getDomains(),
      'filter_type': filterType,
      'filter_ids': filter_ids,
      'chart_year': parseInt(ES_YEAR),
      'record_count': SNO,
      'le_ids': chartInput.getLegalEntities()
    };
    client_mirror.getEscalationDrillDown(requestData, function (status, data) {
      escalationDrilldowndelayed('delayed', data);
      escalationDrilldownnotcomplied('not_complied', data);
    });
  } else if (getcharttype == 'not_complied') {
    var filter_type = chartInput.getFilterType();
    var filter_ids = getFilterIds(filter_type);
    var filterType = filter_type.replace('_', '-');
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == 'Group') {
      filter_ids = chartInput.getCountries();
    }
    var requestData = {
      'd_ids': chartInput.getDomains(),
      'filter_type': filterType,
      'filter_ids': filter_ids,
      'not_complied_type': NC_TYPE,
      'record_count': SNO,      
      'le_ids': chartInput.getLegalEntities()
    };
    client_mirror.getNotCompliedDrillDown(requestData, function (status, data) {
      notCompliedDrilldown('not_complied', data.n_drill_down_data);
    });
  } else if (getcharttype == 'trend_chart') {
    var filter_type = chartInput.getFilterType();
    var filter_ids = getFilterIds(filter_type);
    var filterType = filter_type.replace('_', '-');
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == 'Group') {
      filter_ids = chartInput.getCountries();
    }
    console.log("year: " + chartInput.chartYear);
    
    var year = chartInput.chartYear;
    var requestData = {
      'c_ids': chartInput.getCountries(),
      'd_ids': chartInput.getDomains(),
      'filter_type': filterType,
      'filter_ids': filter_ids,
      'year': parseInt(year),
      'le_ids': chartInput.getLegalEntities()
    };
    $('.btn-back').on('click', function () {
      $('.chart-container').show();
      $('.div-drilldown-container').hide();
      $('.div-assignee-wise-compliance').hide();
      loadTrendChart();
    });
    client_mirror.getTrendChartDrillDown(requestData, function (status, data) {
      TREND_CHART_DATA = data;
      updateTrendChartDrillDown(status, data, year);
    });
  } else if (getcharttype == 'applicability_status') {
    var filter_type = chartInput.getFilterType();
    filter_ids = getFilterIds(filter_type);
    var filterType = filter_type.replace('_', '-');
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == 'Group') {
      filter_ids = chartInput.getCountries();
    }
    var requestData = {
      'c_ids': chartInput.getCountries(),
      'd_ids': chartInput.getDomains(),
      'filter_type': filterType,
      'filter_ids': filter_ids,
      'applicability_status': CAS_TYPE,
      'record_count': SNO,      
      'le_ids': chartInput.getLegalEntities()
    };
    client_mirror.getComplianceApplicabilityDrillDown(requestData, function (status, data) {
      if (data.r_drill_down_data == '') {
        $('#pagination').hide();
      }
      showComplianceApplicabilityDrillDownRecord(data, CAS_TYPE);
    });
  }
}
function showComplianceApplicabilityDrillDownRecord_headingList() {
  var tableHeading = $('#templates .compliance-applicable-status .div-compliance-applicable-list');
  var cloneHeading = tableHeading.clone();
  $('.drilldown-container').append(cloneHeading);    
}
function showComplianceApplicabilityDrillDownRecord_level1List(data) {
  console.log(data.level1_name);
  if (CAS_LEVEL1 != data.level1_name) {
    var tableLevel1 = $('#templates .compliance-applicable-status .table-row-accordian-unit .table-heading tbody');
    var cloneLevel1 = tableLevel1.clone();
    $('.level1-heading', cloneLevel1).html(data.level1_name);
    $('.panel-title td', cloneLevel1).attr('href', '#collapse' + ACCORDIONCOUNT);
    $('.panel-title td', cloneLevel1).attr('aria-controls', 'collapse' + ACCORDIONCOUNT);
    if (ACCORDIONCOUNT == 1) { //For First group open collapse
        $('.panel-title td', cloneLevel1).attr('aria-expanded', true);
        $('.panel-title td', cloneLevel1).removeClass('collapsed');
        $('.coll-title', cloneLevel1).addClass('in');
    }
    $('.drilldown-container .div-compliance-applicable-list').append(cloneLevel1);

    var tableActTbody = $('#templates .compliance-applicable-status .table-row-accordian-unit .compliance-list-inner tbody');
    var cloneActTbody = tableActTbody.clone();
    cloneActTbody.attr('id', 'collapse'+ACCORDIONCOUNT);
    cloneActTbody.attr('aria-labelledb', 'heading'+ACCORDIONCOUNT);
    $('.drilldown-container .div-compliance-applicable-list').append(cloneActTbody);

    CAS_LEVEL1 = data.level1_name;
  }
}
function showComplianceApplicabilityDrillDownRecord_unitList(data) {
  if (CAS_UNITNAME != data.unit_name) {
    var tableUnit = $('#templates .compliance-applicable-status .table-row-accordian .tr-unit');
    var cloneUnit = tableUnit.clone();
    var disp_unitname = '';
    $('.unit-heading span', cloneUnit).html(data.unit_name);
    $('#collapse'+ACCORDIONCOUNT).append(cloneUnit);
    CAS_UNITNAME = data.unit_name;
  }
}
function showComplianceApplicabilityDrillDownRecord_complianceList(val) {  
  SNO = SNO + 1;
  var frequency = val.frequency;
  var statutory_date = val.statu_dates;
  var statutorydate = '';
  var triggerbefore = '';
  var summary = val.summary;
  for (j = 0; j < statutory_date.length; j++) {
    var sDay = '';
    if (statutory_date[j].statutory_date != null)
      sDay = statutory_date[j].statu_date;
    var sMonth = '';
    if (statutory_date[j].statutory_month != null)
      sMonth = statutory_date[j].statu_month;
    var tBefore = '';
    if (statutory_date[j].trigger_before_days != null)
      tBefore = statutory_date[j].trigger_before_days + ' Days';
    if (sMonth != '')
      sMonth = getMonth_IntegertoString(sMonth);
    if(sDay != "" && sMonth != ""){
      statutorydate += sDay + ' - ' + sMonth + ', ';  
    }    
    triggerbefore += tBefore + ', ';
  }
  if (summary != null) {
    if (statutorydate.trim() != '') {
      statutorydate = statutorydate.replace(/,\s*$/, '');
      statutorydate = summary + ' (' + statutorydate + ')';
    } else {
      statutorydate = summary;
    }
  }
  if (triggerbefore != '') {
    triggerbefore = triggerbefore.replace(/,\s*$/, '');
  }
  var tableRow = $('#templates .compliance-applicable-status .table-row-accordian-unit .table-row-accordian .table-row-list');
  var clone = tableRow.clone();
  var cDescription = val.descp;
  var partDescription = cDescription;
  if (cDescription != null && cDescription.length > 50) {
    partDescription = cDescription.substring(0, 49) + '...';
  }
  var cPenalConsequences = val.p_cons;
  var partPenalConsequences = cPenalConsequences;
  if (cPenalConsequences != null && cPenalConsequences.length > 50) {
    partPenalConsequences = cPenalConsequences.substring(0, 49) + '...';
  }
  $('.sno', clone).html(SNO);
  $('.statutory-name', clone).html(val.s_prov);
  var download_url = val.download_url;
  if (download_url == null) {
    $('.compliance-task-name', clone).html(val.comp_name);
  } else {
    $('.compliance-task-name', clone).html('<a href= "' + download_url + '" target="_new">' + val.comp_name + '</a>');
  }
  $('.compliance-description-name', clone).html('<abbr class="page-load" title="' + cDescription + '">' + partDescription + '</abbr>');
  $('.penal-consequences-name', clone).html('<abbr class="page-load" title="' + cPenalConsequences + '">' + partPenalConsequences + '</abbr>');
  $('.compliance-frequency-name', clone).html(frequency);
  $('.repeats', clone).html(statutorydate);
  //$(".statutory-date", clone).html(statutorydate);
  $('.trigger-before', clone).html(triggerbefore);
  console.log(ACCORDIONCOUNT+"^^");
  $('#collapse'+ACCORDIONCOUNT).append(clone);
  
}
function showComplianceApplicabilityDrillDownRecord(data, type) {
  FULLARRAYLIST = [];
  var data = data.r_drill_down_data;
  $.each(data, function (i, val) {
    var level1_Object = {};
    level1_Object.level1_name = val.level1_statutory_name;
    var list_comp = val.ap_compliances;
    FULLARRAYLIST.push(level1_Object);
    $.each(list_comp, function (i1, val1) {
      var unit_Object = {};
      unit_Object.unit_name = i1;
      var list_compliancesDetails = val1;
      val1 = undefined;
      FULLARRAYLIST.push(unit_Object);
      $.each(list_compliancesDetails, function (i2, val2) {
        FULLARRAYLIST.push(val2);
      });
    });
  });
  var totallist = FULLARRAYLIST.length;  
  if(totallist > PAGESIZE){
    $('#pagination').show();
  }
  else{
    $('#pagination').hide();
  }
  //var sub_array_list = get_sub_array(FULLARRAYLIST, STARTCOUNT, ENDCOUNT);
  for (var y = 0; y < totallist; y++) {
    if (Object.keys(FULLARRAYLIST[y])[0] == 'level1_name') {
      ACCORDIONCOUNT++;
      showComplianceApplicabilityDrillDownRecord_level1List(FULLARRAYLIST[y]);
    } else if (Object.keys(FULLARRAYLIST[y])[0] == 'unit_name') {
      showComplianceApplicabilityDrillDownRecord_unitList(FULLARRAYLIST[y]);
    } else if (Object.keys(FULLARRAYLIST[y])[0] == 'comp_id') {
      showComplianceApplicabilityDrillDownRecord_complianceList(FULLARRAYLIST[y]);
    }
  }
}
function showNotCompliedDrillDownRecord(data) {
  $('.drilldown-container').empty();
  $('.escalation-drilldown-container').empty();
  $('.page-title').text('Over due compliances of ' + GROUP_NAME);

   var tableCreate = $('#templates .notcomplied-status .table-not-complied-status');
  var clonetablecreate = tableCreate.clone();
  $('.drilldown-container').append(clonetablecreate);

  // var tableHeading = $('#templates .notComplied-status .tr-heading');
  // var cloneHeading = tableHeading.clone();
  // $('.table-thead-drilldown-list').append(cloneHeading);
  var tableFilter = $('#templates .notComplied-status .tr-filter');
  var cloneFilter = tableFilter.clone();
  $('.table-thead-drilldown-list').append(cloneFilter);

  var data = data.n_drill_down_data;
  var filter_type = chartInput.getFilterType();
  if (filter_type == 'group') {
    groupWiseNotCompliedDrillDown('not_complied', data);
  }
  if (filter_type == 'business_group') {
    businessgroupWiseNotCompliedDrillDown('not_complied', data);
  }
  if (filter_type == 'legal_entity') {
    legalentityWiseNotCompliedDrillDown('not_complied', data);
  }
  if (filter_type == 'division') {
    divisionWiseNotCompliedDrillDown('not_complied', data);
  }
  if (filter_type == 'unit') {
    unitWiseNotCompliedDrillDown('not_complied', data);
  }
}
function groupWiseNotCompliedDrillDown(status, data) {
  $('.business-group-row').show();
  $('.businessgroup-name').show();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  $('.tr-level1 td').attr('colspan', '8');
  $('.panel-title td').attr('colspan', '7');
  notCompliedDrilldown(status, data);
}
function businessgroupWiseNotCompliedDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  $('.tr-level1 td').attr('colspan', '7');
  $('.panel-title td').attr('colspan', '6');
  notCompliedDrilldown(status, data);
}
function legalentityWiseNotCompliedDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').show();
  $('.division-name').show();
  $('.tr-level1 td').attr('colspan', '6');
  $('.panel-title td').attr('colspan', '5');
  notCompliedDrilldown(status, data);
}
function divisionWiseNotCompliedDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  $('.tr-level1 td').attr('colspan', '5');
  $('.panel-title td').attr('colspan', '4');
  notCompliedDrilldown(status, data);
}
function unitWiseNotCompliedDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  $('.tr-level1 td').attr('colspan', '5');
  $('.panel-title td').attr('colspan', '4');
  notCompliedDrilldown(status, data);
}
function notCompliedDrilldown(status, data) {
  $('.btn-back').on('click', function () {
    $('.chart-container').hide();
    $('.div-drilldown-container').hide();
    $('.drilldown-container').hide();
    $('.div-assignee-wise-compliance').hide();
    loadNotCompliedChart();
  });
  if (data == '') {
    $('#pagination').hide();
  }
  ACCORDIONCOUNT = 0;
  $.each(data, function (key, value) {

    if (NC_UNITNAME != value.u_name) {
      ACCORDIONCOUNT = ACCORDIONCOUNT + 1;
      var tableUnit = $('#templates .notcomplied-status .table-row-accordian-unit table tbody');
      var cloneUnit = tableUnit.clone();
      $('.unit-heading', cloneUnit).html(value.u_name);
      $('.panel-title td', cloneUnit).attr('href', '#collapse' + ACCORDIONCOUNT);
      $('.panel-title td', cloneUnit).attr('aria-controls', 'collapse' + ACCORDIONCOUNT);
      if (ACCORDIONCOUNT == 1) { //For First group open collapse
          $('.panel-title td', cloneUnit).attr('aria-expanded', true);
          $('.panel-title td', cloneUnit).removeClass('collapsed');
         
      }
      $('.drilldown-container .div-notcomplied-list').append(cloneUnit);

      var tableActTbody = $('#templates .notcomplied-status .table-row-accordian-unit .compliance-list-inner tbody');
      var cloneActTbody = tableActTbody.clone();
      cloneActTbody.attr('id', 'collapse'+ACCORDIONCOUNT);
      cloneActTbody.attr('aria-labelledb', 'heading'+ACCORDIONCOUNT);
      if (ACCORDIONCOUNT == 1) {
         cloneActTbody.addClass('in');
      }
      $('.drilldown-container .div-notcomplied-list').append(cloneActTbody);

      NC_UNITNAME = value.u_name;
    }
    var unitList = value.drill_compliances;
    $.each(unitList, function (ke, valu) {
      if (NC_LEVEL1 != ke) {
        var tableLevel1 = $('#templates .notcomplied-status .table-row-list .tr-level1');
        var cloneLevel1 = tableLevel1.clone();
        $('.heading', cloneLevel1).html(ke);
        $(' #collapse'+ACCORDIONCOUNT).append(cloneLevel1);
        NC_LEVEL1 = ke;
      }
      $.each(valu, function (k, val) {
        SNO = SNO + 1;
        var tableRow = $('#templates .notcomplied-status .table-row-list .tr-compliance');
        var clone = tableRow.clone();
        $('.sno', clone).html(SNO);
        $('.businessgroup-name', clone).html(value.bg_name);
        $('.legalentity-name', clone).html(value.le_name);
        $('.division-name', clone).html(value.div_name);
        // $('.industry-type-name', clone).html(value.indus_name);
        $('.compliance-name', clone).html(val.comp_name);
        $('.assigned-to', clone).html(val.assignee_name);
        $('.over-due', clone).html(val.ageing);
        $('#collapse'+ACCORDIONCOUNT).append(clone);
      });
    });
  });
  // accordianType('accordion', 'accordion-toggle', 'accordion-content');
  $('.js-filtertable').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter');
  });
  $('.js-filtertable_not_c').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter_not_c');
  });
}
function showEscalationDrillDownRecord(data, year) {
  var filter_type = chartInput.getFilterType();
  $('.div-assignee-wise-compliance').hide();
  $('.drilldown-container').empty();
  $('.escalation-drilldown-container').empty();
  $('.assignee-wise').hide();
  $('.page-title').text('Escalations of ' + GROUP_NAME + ' for the year ' + year);
  if (filter_type == 'group') {
    groupWiseEscalationDrillDown('delayed', data);
    groupWiseEscalationDrillDown('not_complied', data);
  }
  if (filter_type == 'business_group') {
    businessgroupWiseEscalationDrillDown('delayed', data);
    businessgroupWiseEscalationDrillDown('not_complied', data);
  }
  if (filter_type == 'legal_entity') {
    legalentityWiseEscalationDrillDown('delayed', data);
    legalentityWiseEscalationDrillDown('not_complied', data);
  }
  if (filter_type == 'division') {
    divisionWiseEscalationDrillDown('delayed', data);
    divisionWiseEscalationDrillDown('not_complied', data);
  }
  if (filter_type == 'unit') {
    unitWiseEscalationDrillDown('delayed', data);
    unitWiseEscalationDrillDown('not_complied', data);
  }  //$(".td-escalation").empty();
}
function groupWiseEscalationDrillDown(status, data) {
  $('.business-group-row').show();
  $('.businessgroup-name').show();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  if (status == 'not_complied') {
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '8');
    $('.delayed-by-row').hide();
    $('.over-due-row').show();
  } else if (status == 'delayed') {
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '7');
    $('.delayed-by-row').show();
    $('.over-due-row').hide();
  }
  escalationDrilldown(status, data);
}
function businessgroupWiseEscalationDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  if (status == 'not_complied') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '7');
    $('.delayed-by-row').hide();
    $('.over-due-row').show();
  } else if (status == 'delayed') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '6');
    $('.delayed-by-row').show();
    $('.over-due-row').hide();
  }
  escalationDrilldown(status, data);
}
function legalentityWiseEscalationDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').show();
  $('.division-name').show();
  if (status == 'not_complied') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '5');
    $('.over-due-row').show();
    $('.delayed-by-row').hide();
  } else if (status == 'delayed') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '5');
    $('.delayed-by-row').show();
    $('.over-due-row').hide();
  }
  escalationDrilldown(status, data);
}
function divisionWiseEscalationDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  if (status == 'not_complied') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.over-due-row').show();
    $('.delayed-by-row').hide();
  } else if (status == 'delayed') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.delayed-by-row').show();
    $('.over-due-row').hide();
  }
  escalationDrilldown(status, data);
}
function unitWiseEscalationDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  if (status == 'not_complied') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.over-due-row').show();
    $('.delayed-by-row').hide();  //var status = "Not Complied"
  } else if (status == 'delayed') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.delayed-by-row').show();
    $('.over-due-row').hide();  //var status = "Delayed"
  }
  escalationDrilldown(status, data);
}
function escalationDrilldown(status, data) {
  if (status == 'not_complied') {
    if (ES_NC_COUNT == 1) {
      var h2heading = $('#templates .escalation-status .table-row-accordian-unit .tr-h2');
      var cloneh2 = h2heading.clone();
      //$('.escalation-status-text span', cloneh2).css({ 'margin-top': '40px' });
      $('.escalation-status-text span', cloneh2).html('Not Complied compliances');
      $('.drilldown-container').append(cloneh2);

      var tableHeading = $('#templates .escalation-status .table-escalation-status');
      var cloneHeading = tableHeading.clone();
      $('.drilldown-container').append(cloneHeading);

      // var tableFilter = $('#templates .escalation-status .tr-filter');
      // var cloneFilter = tableFilter.clone();
      // $('.thead-itncel').append(cloneFilter);
      // $('.inner-table-notcomplied-escalation-list .business-group-row .filter-text-box').addClass('js-filter_not_c');
      // $('.inner-table-notcomplied-escalation-list .legal-entity-row .filter-text-box').addClass('js-filter_not_c');
      // $('.inner-table-notcomplied-escalation-list .division-row .filter-text-box').addClass('js-filter_not_c');
      // $('.inner-table-notcomplied-escalation-list .type-row .filter-text-box').addClass('js-filter_not_c');
      // $('.inner-table-notcomplied-escalation-list .compliance-row .filter-text-box').addClass('js-filter_not_c');
      // $('.inner-table-notcomplied-escalation-list .assigned-to-row .filter-text-box').addClass('js-filter_not_c');
      // $('.inner-table-notcomplied-escalation-list .over-due-row .filter-text-box').addClass('js-filter_not_c');
      ES_NC_COUNT++;
    }
    escalationDrilldownnotcomplied('not_complied', data);
  }
  if (status == 'delayed') {
    if (ES_D_COUNT == 1) {
      var h2heading = $('#templates .delayed-escalation-status .table-row-accordian-unit .tr-h2');
      var cloneh2 = h2heading.clone();
      //$('.escalation-status-text span', cloneh2).css({ 'margin-top': '40px' });
      $('.escalation-status-text span', cloneh2).html('Delayed compliances');
      $('.escalation-drilldown-container').append(cloneh2);

      var tableHeading = $('#templates .delayed-escalation-status .table-delayed-escalation-status');
      var cloneHeading = tableHeading.clone();
      $('.escalation-drilldown-container').append(cloneHeading);

      // var h2heading = $('#templates .escalation-status .tr-h2');
      // var cloneh2 = h2heading.clone();
      // $('.escalation-status-value', cloneh2).html('Delayed compliances');
      // $('.thead-itdel').append(cloneh2);

      // var tableHeading = $('#templates .escalation-status .tr-heading');
      // var cloneHeading = tableHeading.clone();
      // $('.thead-itdel').append(cloneHeading);

      // var tableFilter = $('#templates .escalation-status .tr-filter');
      // var cloneFilter = tableFilter.clone();
      // $('.thead-itdel').append(cloneFilter);
      // $('.inner-table-delayed-escalation-list .business-group-row .filter-text-box').addClass('js-filter_delayed');
      // $('.inner-table-delayed-escalation-list .legal-entity-row .filter-text-box').addClass('js-filter_delayed');
      // $('.inner-table-delayed-escalation-list .division-row .filter-text-box').addClass('js-filter_delayed');
      // // $('.inner-table-delayed-escalation-list .type-row .filter-text-box').addClass('js-filter_delayed');
      // $('.inner-table-delayed-escalation-list .compliance-row .filter-text-box').addClass('js-filter_delayed');
      // $('.inner-table-delayed-escalation-list .assigned-to-row .filter-text-box').addClass('js-filter_delayed');
      // $('.inner-table-delayed-escalation-list .delayed-by-row .filter-text-box').addClass('js-filter_delayed');
      ES_D_COUNT++;
    }
    escalationDrilldowndelayed('delayed', data);
  }
}
function escalationDrilldownnotcomplied(status, data) {
  if (data[status] == '') {
    $('#pagination').hide();
  } else {
    $('#pagination').show();
  }
  if (typeof data[status] != 'undefined') {
    $.each(data[status], function (key, value) {
      if (ES_NC_UNITNAME != value.u_name) {
        ACCORDIONCOUNTNC = ACCORDIONCOUNTNC + 1;
        var tableUnit = $('#templates .escalation-status .unit-title');
        var cloneUnit = tableUnit.clone();
        $('.unit-heading', cloneUnit).html(value.u_name);
        $('.panel-title td', cloneUnit).attr('href', '#collapse' + ACCORDIONCOUNTNC);
        $('.panel-title td', cloneUnit).attr('aria-controls', 'collapse' + ACCORDIONCOUNTNC);
        if (ACCORDIONCOUNTNC == 1) { //For First group open collapse
            $('.panel-title td', cloneUnit).attr('aria-expanded', true);
            $('.panel-title td', cloneUnit).removeClass('collapsed');
            $('.coll-title', cloneUnit).addClass('in');
        }
        $('.drilldown-container .div-escalation-list').append(cloneUnit);
        
        var tableActTbody = $('#templates .escalation-status .table-row-accordian-unit .compliance-list-inner tbody');
        var cloneActTbody = tableActTbody.clone();
        cloneActTbody.attr('id', 'collapse'+ACCORDIONCOUNTNC);
        cloneActTbody.attr('aria-labelledb', 'heading'+ACCORDIONCOUNTNC);
        $('.drilldown-container .div-escalation-list').append(cloneActTbody);
        ES_NC_UNITNAME = value.u_name;
      }
      var unitList = value.drill_compliances;
      $.each(unitList, function (ke, valu) {
        if (ES_NC_LEVEL1 != ke) {
          var tableLevel1 = $('#templates .escalation-status .tr-level1');
          var cloneLevel1 = tableLevel1.clone();
          $('.heading', cloneLevel1).html(ke);
          $('#collapse'+ACCORDIONCOUNTNC).append(cloneLevel1);
          ES_NC_LEVEL1 = ke;
        }
        $.each(valu, function (k, val) {
          SNO = SNO + 1;
          var tableRow = $('#templates .escalation-status .table-row-list .tr-compliance');
          var clone = tableRow.clone();
          $('.sno', clone).html(SNO);
          $('.businessgroup-name', clone).html(value.bg_name);
          $('.legalentity-name', clone).html(value.le_name);
          $('.division-name', clone).html(value.div_name);
          // $('.industry-type-name', clone).html(value.indus_name);
          $('.compliance-name', clone).html(val.comp_name);
          $('.assigned-to', clone).html(val.assignee_name);
          if (val.status == 'Delayed Compliance') {
            $('.delayed-by', clone).html(val.ageing);
          }
          if (val.status == 'Not Complied') {
            $('.over-due', clone).html(val.ageing);
          }
          $('#collapse'+ACCORDIONCOUNTNC).append(clone);
        });
      });
    });
  }
  else{
    var tableRow = $('#templates .escalation-status .norecords-list');
    var clone = tableRow.clone();
    $('.norecord', clone).html("No Record Found");
    $('.inner-table-notcomplied-escalation-list').append(clone);
  }
  $('.js-filtertable').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter');
  });
  $('.js-filtertable_not_c').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter_not_c');
  });
}
function escalationDrilldowndelayed(status, data) {
  if (data[status] == '') {
    $('#pagination').hide();    
  } else {
    $('#pagination').show();
  }
  if (typeof data[status] != 'undefined') {
    $.each(data[status], function (key, value) {
      if (ES_D_UNITNAME != value.u_name) {
        ACCORDIONCOUNTD = ACCORDIONCOUNTD + 1;
        var tableUnit = $('#templates .delayed-escalation-status .unit-title');
        var cloneUnit = tableUnit.clone();
        $('.unit-heading', cloneUnit).html(value.u_name);
        $('.panel-title td', cloneUnit).attr('href', '#collapseDelay' + ACCORDIONCOUNTD);
        $('.panel-title td', cloneUnit).attr('aria-controls', 'collapseDelay' + ACCORDIONCOUNTD);
        if (ACCORDIONCOUNTD == 1) {
            $('.panel-title td', cloneUnit).attr('aria-expanded', true);
            $('.panel-title td', cloneUnit).removeClass('collapsed');
            $('.coll-title', cloneUnit).addClass('in');
        }
        $('.escalation-drilldown-container .div-delayed-escalation-list').append(cloneUnit);

        var tableActTbody = $('#templates .delayed-escalation-status .table-row-accordian-unit .compliance-list-inner tbody');
        var cloneActTbody = tableActTbody.clone();
        cloneActTbody.attr('id', 'collapseDelay'+ACCORDIONCOUNTD);
        cloneActTbody.attr('aria-labelledb', 'heading'+ACCORDIONCOUNTD);
        $('.escalation-drilldown-container .div-delayed-escalation-list').append(cloneActTbody);

        ES_D_UNITNAME = value.u_name;
      }
      var unitList = value.drill_compliances;
      $.each(unitList, function (ke, valu) {
        if (ES_D_LEVEL1 != ke) {
          var tableLevel1 = $('#templates .delayed-escalation-status .tr-level1');
          var cloneLevel1 = tableLevel1.clone();
          $('.heading', cloneLevel1).html(ke);
          $('#collapseDelay'+ACCORDIONCOUNTD).append(cloneLevel1);
          ES_D_LEVEL1 = ke;
        }
        $.each(valu, function (k, val) {
          SNO = SNO + 1;
          var tableRow = $('#templates .delayed-escalation-status .table-row-list .tr-compliance');
          var clone = tableRow.clone();
          $('.sno', clone).html(SNO);
          $('.businessgroup-name', clone).html(value.bg_name);
          $('.legalentity-name', clone).html(value.le_name);
          $('.division-name', clone).html(value.div_name);
          // $('.industry-type-name', clone).html(value.industry_name);
          $('.compliance-name', clone).html(val.comp_name);
          $('.assigned-to', clone).html(val.assignee_name);
          if (val.status == 'Delayed Compliance') {
            $('.delayed-by', clone).html(val.ageing);
          }
          if (val.status == 'Not Complied') {
            $('.over-due', clone).html(val.ageing);
          }
          $('#collapseDelay'+ACCORDIONCOUNTD).append(clone);
        });
      });
    });
  }
  // else{
  //     var tableRow = $('#templates .escalation-status .norecords-list');
  //     var clone = tableRow.clone();
  //     $('.norecord', clone).html("No Record Found");
  //     $('.inner-table-delayed-escalation-list').append(clone);
  // }
  //accordianTypedelayed('accordionD', 'accordion-toggle', 'accordion-delayed-content');
  $('.js-filtertable').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter');
  });
  $('.js-filtertable-delayed').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter-delayed');
  });
}
// function accordianTypedelayed(idtype, toggleClass, contentClass) {
//   $('#' + idtype).find('.' + toggleClass).click(function () {
//     $(this).next().slideToggle('fast');
//     $('.' + contentClass).not($(this).next()).slideUp('fast');
//   });
// }
// function accordianTypenotcomplied(idtype, toggleClass, contentClass) {
//   $('#' + idtype).find('.' + toggleClass).click(function () {
//     $(this).next().slideToggle('fast');
//     $('.' + contentClass).not($(this).next()).slideUp('fast');
//   });
// }
// Trend Chart Drill Down
function updateTrendChartDrillDown(status, data, year) {
  $('.chart-container').hide();
  $('.graph-selections-bottom').hide();
  $('.div-drilldown-container').show();
  $('.drilldown-container').show();
  $('.escalation-drilldown-container').empty();
  $('.div-assignee-wise-compliance').hide();
  $('.btn-back').show();
 
  showTrendChartDrillDownRecord(status, data, year);
}
function showTrendChartDrillDownRecord(status, data, year) {
  $('.page-title').text('Trend Chart of the ' + year);
  var data = data.t_drill_down_data;
  // var tableHeading = $('#templates .compliance-status .tr-heading');
  // var cloneHeading = tableHeading.clone();
  // $('.table-thead-drilldown-list').append(cloneHeading);
  // var tableFilter = $('#templates .compliance-status .tr-filter');
  // var cloneFilter = tableFilter.clone();
  // $('.table-thead-drilldown-list').append(cloneFilter);
  var filter_type = chartInput.getFilterType();
  if (filter_type == 'group') {
    groupWiseTrendChartDrillDown(status, data);
  }
  if (filter_type == 'business_group') {
    businessgroupWiseTrendChartDrillDown(status, data);
  }
  if (filter_type == 'legal_entity') {
    legalentityWiseTrendChartDrillDown(status, data);
  }
  if (filter_type == 'division') {
    divisionWiseTrendChartDrillDown(status, data);
  }
  if (filter_type == 'unit') {
    unitWiseTrendChartDrillDown(status, data);
  }
}
function groupWiseTrendChartDrillDown(status, data) {  
  $('.drilldown-container').empty();
  $('.business-group-row').show();
  $('.businessgroup-name').show();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '7');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '7');
    $('.over-due-row').show();
  } else if (status == 'Delayed') {
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '7');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '7');
    $('.tr-unit tr th').attr('colspan', '6');
  }
  trendChartDrilldown(status, data);
}
function businessgroupWiseTrendChartDrillDown(status, data) {
  $('.drilldown-container').empty();
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '6');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '6');
    $('.over-due-row').show();
  } else if (status == 'Delayed') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '6');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '6');
    $('.tr-unit tr th').attr('colspan', '5');
  }
  trendChartDrilldown(status, data);
}
function legalentityWiseTrendChartDrillDown(status, data) {
  $('.drilldown-container').empty();
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').show();
  $('.division-name').show();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '5');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '5');
    $('.over-due-row').show();
  } else if (status == 'Delayed') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '5');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '5');
    $('.tr-unit tr th').attr('colspan', '4');
  }
  trendChartDrilldown(status, data);
}
function divisionWiseTrendChartDrillDown(status, data) {
  $('.drilldown-container').empty();
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.over-due-row').show();
  } else if (status == 'Delayed') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '4');
    $('.tr-unit tr th').attr('colspan', '3');
  }
  trendChartDrilldown(status, data);
}
function unitWiseTrendChartDrillDown(status, data) {
  $('.drilldown-container').empty();
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.over-due-row').show();
  } else if (status == 'Delayed') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '4');
    $('.tr-unit tr th').attr('colspan', '3');
  }
  trendChartDrilldown(status, data);
}
function trendChartDrilldown(status, data) {

  var tableCreate = $('#templates .compliance-status .table-compliance-status');
  var clonetablecreate = tableCreate.clone();
  $('.drilldown-container').append(clonetablecreate);

  var actCount = 0;
  $.each(data, function (key, value) {
    if (TC_UNIT != value.u_name) {
      actCount++;
      var tableUnit = $('#templates .compliance-status .table-row-accordian-unit table tbody');
      var cloneUnit = tableUnit.clone();
      $('.unit-heading', cloneUnit).html(value.u_name);
      $('.panel-title td', cloneUnit).attr('href', '#collapse' + actCount);
      $('.panel-title td', cloneUnit).attr('aria-controls', 'collapse' + actCount);
      if (actCount == 1) { //For First group open collapse
          $('.panel-title td', cloneUnit).attr('aria-expanded', true);
          $('.panel-title td', cloneUnit).removeClass('collapsed');
          $('.coll-title', cloneUnit).addClass('in');
      }
      $('.drilldown-container  .div-compliance-list').append(cloneUnit);

      var tableActTbody = $('#templates .compliance-status .table-row-accordian-unit .compliance-list-inner tbody');
      var cloneActTbody = tableActTbody.clone();
      cloneActTbody.attr('id', 'collapse'+actCount);
      cloneActTbody.attr('aria-labelledb', 'heading'+actCount);
      $('.drilldown-container .div-compliance-list').append(cloneActTbody);
      TC_UNIT = value.unit_name;
    }

    // if (TC_UNIT != value.unit_name) {
    //   ACCORDIONCOUNT = ACCORDIONCOUNT + 1;
    //   var tableUnit = $('#templates .compliance-status .tr-unit');
    //   var cloneUnit = tableUnit.clone();
    //   $('.unit-heading', cloneUnit).html(value.unit_name);
    //   $('.table-drilldown-list').append(cloneUnit);
    //   $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content' + ACCORDIONCOUNT + '"></tbody>');
    //   if (ACCORDIONCOUNT == 1) {
    //     $('.accordion-content' + ACCORDIONCOUNT).addClass('default');
    //   }
    //   TC_UNIT = value.unit_name;
    // }
    var unitList = value.t_compliances;
    $.each(unitList, function (ke, valu) {
      if (TC_LEVEL1 != ke) {
        var tableLevel1 = $('#templates .compliance-status .table-row-list .tr-level1');
        var cloneLevel1 = tableLevel1.clone();
        $('.heading', cloneLevel1).html(ke);
        $(' #collapse'+actCount).append(cloneLevel1);
        CS_LAST_LEVEL1 = ke;
        TC_LEVEL1 = ke;
      }
      $.each(valu, function (k, val) {
        SNO = SNO + 1;
        var tableRow = $('#templates .compliance-status .table-row-list .tr-compliance');
        var clone = tableRow.clone();
        $('.sno', clone).html(SNO);
        $('.businessgroup-name', clone).html(value.bg_name);
        $('.legalentity-name', clone).html(value.le_name);
        $('.division-name', clone).html(value.div_name);
        // $('.industry-type-name', clone).html(value.i_name);
        $('.compliance-name', clone).html(val.comp_name);
        $('.assigned-to', clone).html(val.assignee_name);
        
        $(' #collapse'+actCount).append(clone);
      });
    });
  });
  // accordianType('accordion', 'accordion-toggle', 'accordion-content');
  $('.js-filtertable').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter');
  });
}
function showDrillDownRecord(status, data, filterTypeName) {
  console.log("Enter showDrillDownRecord");
  $("#pagination").hide();
  $(".chart-container").hide();
  $(".div-drilldown-container").show();
  $(".drilldown-container").show();
  $('.div-assignee-wise-compliance').hide();
  $(".drilldown-container").empty();
  $(".assignee-wise").hide();
  $('.escalation-drilldown-container').empty();

  var data = data.drill_down_data;
  var tableCreate = $('#templates .compliance-status .table-compliance-status');
  var clonetablecreate = tableCreate.clone();
  $('.drilldown-container').append(clonetablecreate);

  var filter_type = chartInput.getFilterType();
  if (filter_type == 'group') {
    groupWiseComplianceDrillDown(status, data);
    drilldownTitleText = 'Compliances - Country: ' + filterTypeName + ', Status: ' + status;
  }
  if (filter_type == 'business_group') {
    businessgroupWiseComplianceDrillDown(status, data);
    drilldownTitleText = 'Compliances - Business Group: ' + filterTypeName + ', Status: ' + status;
  }
  if (filter_type == 'legal_entity') {
    legalentityWiseComplianceDrillDown(status, data);
    drilldownTitleText = 'Compliances - Legal Entity: ' + filterTypeName + ', Status: ' + status;
  }
  if (filter_type == 'division') {
    divisionWiseComplianceDrillDown(status, data);
    drilldownTitleText = 'Compliances - Division: ' + filterTypeName + ', Status: ' + status;
  }
  if (filter_type == 'unit') {
    unitWiseComplianceDrillDown(status, data);
    drilldownTitleText = 'Compliances - Unit: ' + filterTypeName + ', Status: ' + status;
  }
 
  // var tableHeading = $('#templates .compliance-status .tr-heading');
  // var cloneHeading = tableHeading.clone();
  // $('.table-thead-drilldown-list').append(cloneHeading);
  // var tableFilter = $('#templates .compliance-status .tr-filter');
  // var cloneFilter = tableFilter.clone();
  // $('.table-thead-drilldown-list').append(cloneFilter);
  $('.page-title').text(drilldownTitleText);
}
function groupWiseComplianceDrillDown(status, data) {

  $('.business-group-row').show();
  $('.businessgroup-name').show();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  console.log(status);
  if (status == 'Inprogress') {
    $('.panel-title td').attr('colspan', '8');
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '8');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.panel-title td').attr('colspan', '8');
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '8');
    $('.over-due-row').show();
  } else if (status == 'Delayed Compliance') {
    $('.panel-title td').attr('colspan', '8');
    $('.tr-level1 td').attr('colspan', '8');
    $('.panel-title td').attr('colspan', '8');
    $('.delayed-by-row').show();
  } else {
    $('.panel-title td').attr('colspan', '7');
    $('.tr-level1 td').attr('colspan', '7');
    $('.tr-unit tr th').attr('colspan', '7');
  }
  complianceStatusDrilldown(status, data);
}
function businessgroupWiseComplianceDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').show();
  $('.legalentity-name').show();
  $('.division-row').show();
  $('.division-name').show();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '7');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '7');
    $('.over-due-row').show();
  } else if (status == 'Delayed Compliance') {
    $('.tr-level1 td').attr('colspan', '7');
    $('.panel-title td').attr('colspan', '7');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '6');
    $('.tr-unit tr th').attr('colspan', '6');
  }
  complianceStatusDrilldown(status, data);
}
function legalentityWiseComplianceDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').show();
  $('.division-name').show();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '6');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '6');
    $('.over-due-row').show();
  } else if (status == 'Delayed Compliance') {
    $('.tr-level1 td').attr('colspan', '6');
    $('.panel-title td').attr('colspan', '6');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '6');
    $('.tr-unit tr th').attr('colspan', '5');
  }
  complianceStatusDrilldown(status, data);
}
function divisionWiseComplianceDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.over-due-row').show();
  } else if (status == 'Delayed Compliance') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '4');
    $('.tr-unit tr th').attr('colspan', '3');
  }
  complianceStatusDrilldown(status, data);
}
function unitWiseComplianceDrillDown(status, data) {
  $('.business-group-row').hide();
  $('.businessgroup-name').hide();
  $('.legal-entity-row').hide();
  $('.legalentity-name').hide();
  $('.division-row').hide();
  $('.division-name').hide();
  $('.delayed-by-row').hide();
  $('.dates-left-to-complete-row').hide();
  $('.over-due-row').hide();
  if (status == 'Inprogress') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.dates-left-to-complete-row').show();
  } else if (status == 'Not Complied') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.over-due-row').show();
  } else if (status == 'Delayed Compliance') {
    $('.tr-level1 td').attr('colspan', '5');
    $('.panel-title td').attr('colspan', '4');
    $('.delayed-by-row').show();
  } else {
    $('.tr-level1 td').attr('colspan', '4');
    $('.tr-unit tr th').attr('colspan', '3');
  }
  complianceStatusDrilldown(status, data);
}
function complianceStatusDrilldown(status, data) {
  if (data == '') {
    $('#pagination').hide();
  }
  var actCount = 0;  
  $.each(data, function (key, value) {
    if (CS_LAST_UNITNAME != value.u_name) {
      actCount++;
      var tableUnit = $('#templates .compliance-status .table-row-accordian-unit table tbody');
      var cloneUnit = tableUnit.clone();
      $('.unit-heading', cloneUnit).html(value.u_name);
      $('.panel-title td', cloneUnit).attr('href', '#collapse' + actCount);
      $('.panel-title td', cloneUnit).attr('aria-controls', 'collapse' + actCount);
      if (actCount == 1) { //For First group open collapse
          $('.panel-title td', cloneUnit).attr('aria-expanded', true);
          $('.panel-title td', cloneUnit).removeClass('collapsed');          
      }
      $('.div-drilldown-container').find('.div-compliance-list').append(cloneUnit);

      var tableActTbody = $('#templates .compliance-status .table-row-accordian-unit .compliance-list-inner tbody');
      var cloneActTbody = tableActTbody.clone();
      cloneActTbody.attr('id', 'collapse'+actCount);
      if (actCount == 1) {
        cloneActTbody.addClass('in');
      }
      cloneActTbody.attr('aria-labelledb', 'heading'+actCount);
      $('.div-drilldown-container').find('.div-compliance-list').append(cloneActTbody);
      CS_LAST_UNITNAME = value.unit_name;
    }
    var unitList = value.drill_compliances;
    $.each(unitList, function (ke, valu) {
      if (CS_LAST_LEVEL1 != ke) {
        var tableLevel1 = $('#templates .compliance-status .table-row-list .tr-level1');
        var cloneLevel1 = tableLevel1.clone();
        $('.heading', cloneLevel1).html(ke);
        $('#collapse'+actCount).append(cloneLevel1);
        CS_LAST_LEVEL1 = ke;
      }
      $.each(valu, function (k, val) {
        SNO = SNO + 1;
        var tableRow = $('#templates .compliance-status .table-row-list .tr-compliance');
        var clone = tableRow.clone();
        $('.sno', clone).html(SNO);
        $('.businessgroup-name', clone).html(value.bg_name);
        $('.legalentity-name', clone).html(value.le_name);
        $('.division-name', clone).html(value.div_name);
        // $('.industry-type-name', clone).html(value.indus_name);
        $('.compliance-name', clone).html(val.comp_name);
        $('.assigned-to', clone).html(val.assignee_name);
        if (val.status == 'Delayed Compliance') {
          $('.delayed-by', clone).html(val.ageing);
        }
        if (val.status == 'Inprogress') {
          $('.dates-left-to-complete', clone).html(val.ageing);
        }
        if (val.status == 'Not Complied') {
          $('.over-due', clone).html(val.ageing);
        }
        $(' #collapse'+actCount).append(clone);
      });
    });
  });
  // accordianType('accordion', 'accordion-toggle', 'accordion-content');
  $('.js-filtertable').on('keyup', function () {
    $(this).filtertable().addFilter('.js-filter');
  });
}
//-----------------------------------End Compliance Status--------------------------------------------------------------
// function accordianType(idtype, toggleClass, contentClass) {
//   $('#' + idtype).find('.' + toggleClass).stop().slideDown('fast');
//   $('#' + idtype).find('.' + toggleClass).click(function (e) {
//     e.preventDefault();
//     e.stopPropagation();
//     $(this).next().slideDown('fast');
//     $('.' + contentClass).not($(this).next()).slideUp('fast');
//   });
// }

function updateAssigneeWiseComplianceFiltersList(data) {
  //$('.table-assignee-wise-compliance-list').hide();
  $('.grid-table-dash1').hide();
  $('.chart-container').hide();
  $('.div-drilldown-container').show();
  $('.drilldown-container').hide();
  $('.escalation-drilldown-container').empty();
  $('.div-assignee-wise-compliance').show();
  $('.assignee-wise').hide();

  // $('.popupoverlay').css('visibility', ' hidden');
  // $('.popupoverlay').css('opacity', '0');
  $('#pagination').hide();
  
  var tableCreate = $('#templates .compliance-report-tab-content');
  var clonetablecreate = tableCreate.clone();
  $('.drilldown-container').append(clonetablecreate);

  COUNTRYLIST = data.countries;
  BUSINESSGROUPSLIST = data.business_groups;
  //LEGALENTITYLIST = data.legal_entities;
  LEGALENTITYLIST = client_mirror.getSelectedLegalEntity();
  DIVISIONLIST = data.client_divisions;
  CATEGORYLIST = data.client_categories;
  UNITLIST = data.units;
  USERLIST = data.users;
}
$("#awc-country").on("keyup",function (e) {
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACCountry, Country, text_val,
    COUNTRYLIST, "c_name", "c_id", function (val) {
      onAutoCompleteSuccess(CountryVal, Country, val);
  });
});

$("#awc-businessgroup").on("keyup",function (e) {
  var text_val = $(this).val();
  console.log(text_val);
  commonAutoComplete(
    e, ACBusinessGroup, BusinessGroup, text_val,
    BUSINESSGROUPSLIST, "bg_name", "bg_id", function (val) {
      onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
  });
});

$("#awc-legalentity").on("keyup",function (e) {
  var text_val = $(this).val();
  console.log(text_val);
  var c_id = Country.val();
  if(c_id == ''){
    displayMessage(message.legalentity_required);
  }  
  var condition_fields = ["c_id"];
  var condition_values = [c_id];
  commonAutoComplete(
    e, ACLegalEntity, LegalEntity, text_val,
    LEGALENTITYLIST, "le_name", "le_id", function (val) {
      onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
  }, condition_fields, condition_values);
});
$("#awc-division").on("keyup",function (e) {
  var text_val = $(this).val();
  var le_id = LegalEntity.val();
  if(le_id == ''){
    displayMessage(message.legalentity_required);
  }  
  var condition_fields = ["le_id"];
  var condition_values = [le_id];
  commonAutoComplete(
    e, ACDivision, Division, text_val,
    DIVISIONLIST, "div_name", "div_id", function (val) {
      onAutoCompleteSuccess(DivisionVal, Division, val);
  }, condition_fields, condition_values);
});
$("#awc-category").on("keyup",function (e) {
  var text_val = $(this).val();
  console.log(text_val);
  if(le_id == ''){
    displayMessage(message.legalentity_required);
  }  
  var condition_fields = ["le_id"];
  var condition_values = [le_id];
  commonAutoComplete(
    e, ACCategory, Category, text_val,
    CATEGORYLIST, "cat_name", "cat_id", function (val) {
      onAutoCompleteSuccess(CategoryVal, Category, val);
  });
});

// $("#awc-category").on("keyup",function (e) {
//   var text_val = $(this).val();
//   console.log(text_val);
//   commonAutoComplete(
//     e, ACCategory, Category, text_val,
//     CATEGORYLIST, "cat_name", "cat_id", function (val) {
//       onAutoCompleteSuccess(CategoryVal, Category, val);
//   });
// });

$("#awc-unit").on("keyup",function (e) {
  var text_val = $(this).val();
  console.log(text_val);
  var le_id = LegalEntity.val();
  if(le_id == ''){
    displayMessage(message.legalentity_required);
  }  
  var condition_fields = ["le_id"];
  var condition_values = [le_id];
  commonAutoComplete(
    e, ACUnit, Unit, text_val,
    UNITLIST, "unit_name", "unit_id", function (val) {
      onAutoCompleteSuccess(UnitVal, Unit, val);
  }, condition_fields, condition_values);
});


$("#awc-user").on("keyup",function (e) {
  var text_val = $(this).val();
  var le_id = LegalEntity.val();
  if(le_id == ''){
    displayMessage(message.legalentity_required);
  }  
  var condition_fields = ["le_id"];
  var condition_values = [le_id];
  console.log(text_val);
  commonAutoComplete(
    e, ACUser, User, text_val,
    USERLIST, "employee_name", "user_id", function (val) {
      onAutoCompleteSuccess(UserVal, User, val);
  }, condition_fields, condition_values);
});


function onAutoCompleteSuccess(value_element, id_element, val) {
console.log(value_element)
console.log(id_element)
  value_element.val(val[1]);
  id_element.val(val[0]);
  value_element.focus();
  var current_id = id_element[0].id;
  console.log(current_id);
  if(current_id == 'c-id'){
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
  }else if(current_id == 'domainid'){
    resetfilter('domian');
  }
  else if(current_id == 'statutoryid'){
    resetfilter('act');
  }
}


function showFiltersResults(csv) {
    var legalentityids = [];
    var country = Country.val().trim();
    var countryval = CountryVal.val().trim();    
    if(countryval == "" || countryval == null){
        displayMessage(message.country_required);
        return false;
    }else{
        var businessgroupid = parseInt(BusinessGroup.val());
        var businessgroupsval = BusinessGroupVal.val().trim();
        if(businessgroupsval == ""){
            businessgroupid = null
        }
        var legalentityid = parseInt(LegalEntity.val().trim());
        var legalentityval = LegalEntityVal.val().trim();
        if(legalentityval == "" ){
            legalentityids = chartInput.getLegalEntities();
        }
        else{
          legalentityids.push(legalentityid)
        }
        var divisionid = parseInt(Division.val().trim());
        var divisionval = DivisionVal.val().trim();
        if(divisionval == ""){
            divisionid = null
        }
        var unitid = parseInt(Unit.val().trim());
        var unitval = UnitVal.val().trim();
        if(unitval == ""){
            unitid = null
        }
        var userid = parseInt(User.val().trim());
        var userval = UserVal.val().trim();
        if(userval == ""){
            userid = null
        }
        displayLoader();
        client_mirror.getAssigneewiseComplianes(
            parseInt(country), businessgroupid, legalentityids,
            divisionid, unitid, userid, csv,
            function (status, data) {
                chart_data = data['assingee_data'];
                download_url = data['link'];
                if(chart_data){
                    updateAssigneeWiseComplianceList(chart_data);
                }else if(download_url){
                    window.open(download_url, '_blank');
                }else{
                }
                hideLoader();
            }
        );
    }
}

function updateAssigneeWiseComplianceList(data) {
  $('.tbody-assignee-wise-compliance-list tr').remove();
  $('.compliance-details-drilldown tr').remove();
  $('.table-assignee-wise-compliance-list').show();
  $('#pagination-assignee').hide();
  $('.compliance_count_assignee').text('');
  $(".assignee-wise").show();
  $(".assignee-wise").empty();
  var aSno = 0;
  var country_assignee = parseInt(Country.val().trim());
  //assingee_data
  var tablethead = $('#templates .report-container-inner .table-assignee-wise-compliance-list');
  var clonethead = tablethead.clone();
  $('.assignee-wise').append(clonethead);

  $.each(data, function (key, value) {
      
    var tableRowHeadingth = $('#templates .assignee-wise-compliance-list .unitHeading');
    var cloneHeadingth = tableRowHeadingth.clone();
    $('.unit-name', cloneHeadingth).text(value.unit_name);
    $('.tbody-assignee-wise-compliance-list').append(cloneHeadingth);

    var assigneewiselist = value.assignee_wise_details;
    $.each(assigneewiselist, function (ke, valu) {
      var tableRow = $('#templates .assignee-wise-compliance-list .userHeading ');
      var clone = tableRow.clone();
      var name_assignee = valu.assignee_name;
      $('.assignee-name-for-popup', clone).html(name_assignee);
      $('.assignee-name-for-popup', clone).click(function() {
        Custombox.open({
            target: '#year-modal',          
            effect:'slit',
            overlaySpeed:100,
            overlayColor:'#36404a',
            complete: function() {
              showPopup(country_assignee, value.unit_id, valu.user_id, valu.assignee_name);
            },
        });
      });
      // $('.assignee-name-for-popup', clone).on('click', function (e) {
      //   //$('#popup-year').show();
      //   showPopup(country_assignee, value.unit_id, valu.user_id, valu.assignee_name);
      // });
      $('.tbody-assignee-wise-compliance-list').append(clone);
      var list = valu.domain_wise_details;
      $.each(list, function (k, val) {
        var domainArr = [];
        var tableRowvalues = $('#templates .assignee-wise-compliance-list .assignee-row-list');
        var cloneval = tableRowvalues.clone();
        aSno++;
        $('.sno', cloneval).text(aSno);
        $('.level1value', cloneval).html(val.domain_name);
        $('.total-count', cloneval).html(val.total_compliances);
        $('.complied-count', cloneval).html(val.complied_count);
        if (val.reassigned_count == 0) {
          $('.delayed-count', cloneval).html(val.assigned_count);
          $('.delayed-count', cloneval).on('click', function (e) {
            $('#popup-reassigned').show();
          });
        } else {
          var delayvalue = val.assigned_count + ' (+' + val.reassigned_count + ')';
          $('.delayed-count', cloneval).html(delayvalue);
          $('.delayed-count', cloneval).addClass('delayedvalue');
          $('.delayedvalue', cloneval).on('click', function (e) {
            $('#popup-reassigned').show();
            showPopupCompDelayed(country_assignee, value.unit_id, valu.user_id, val.domain_id, valu.assignee_name);
          });
        }
        $('.inprogress-count', cloneval).html(val.inprogress_compliance_count);
        $('.not-complied-count', cloneval).html(val.not_complied_count);
        var year = null;
        $('.open-details-list', cloneval).on('click', function (e) {
          updateComplianceList(country_assignee, valu.user_id, val.domain_id, year, value.unit_id, 0, valu.assignee_name, val.domain_name);
        });
        $('.tbody-assignee-wise-compliance-list').append(cloneval);
      });
    });
  });
}
function updateComplianceList(country_id, user_id, domain_id, year, unit_id, start_count, assigneename, domain_name) {
  console.log("domain_id++"+domain_id);
  displayLoader();
  // $('.popupoverlay').css('visibility', 'hidden');
  // $('.popupoverlay').css('opacity', '0');
  $('.table-assignee-wise-compliance-list').hide();
  // $('.grid-table-dash1').show();
  snoAssignee = 0;
  // $('.tbody-assignee-wise-compliance-list tr').remove();
  // $('.compliance-details-drilldown tr').remove();
  // $('.table-assignee-wise-compliance-list').show();

  $(".div-assignee-wise-compliance").hide();
  $(".assignee-wise").hide();

  $('#pagination-assignee').hide();
  $('.compliance_count_assignee').text('');
  $('#a_user').val(user_id);
  $('#a_domain').val(domain_id);
  $('#a_year').val(year);
  $('#a_unit').val(unit_id);

  var tableRowHeadingth = $('#templates .compliance-details-list .filterHeader');
  var cloneHeadingth = tableRowHeadingth.clone();
  $('.comp-list-user', cloneHeadingth).text(assigneename);
  var dispYear = '-';
  var dispDomain = '-';
  if (domain_name != null && domain_name != 'null')
    dispDomain = domain_name;
  if (year != null && year != 'null')
    dispYear = year;
  $('.comp-list-year', cloneHeadingth).text(dispYear);
  $('.comp-list-domain', cloneHeadingth).text(dispDomain);    
  $('.div-assignee-wise-compliance').append(cloneHeadingth);

  legalentityids = chartInput.getLegalEntities(); 
  client_mirror.getAssigneewiseCompliancesDrilldown(country_id, user_id, domain_id, year, unit_id, start_count, legalentityids, function (status, data) {
    listingCompliance(data, user_id, year);
    hideLoader();
  });
}
function getShowmoreData() {
  var country = parseInt($('#country').val().trim());
  var a_user = parseInt($('#a_user').val().trim());
  var a_domain = parseInt($('#a_domain').val().trim());
  var a_year = parseInt($('#a_year').val().trim());
  var a_unit = parseInt($('#a_unit').val().trim());
  client_mirror.getAssigneewiseCompliancesDrilldown(country, a_user, a_domain, a_year, a_unit, snoAssignee, function (status, data) {
    listingCompliance(data, a_user, a_year);
  });
}
function getDomainName(doaminId) {
  var domainName;
  $.each(DOMAINLIST, function (key, value) {
    if (value.domain_id == doaminId) {
      domainName = value.domain_name;
      return false;
    }
  });
  return domainName;
}
function getUserName(userid) {
  var userName;
  $.each(USERLIST, function (key, value) {
    if (value.employee_id == userid) {
      userName = value.employee_name;
      return false;
    }
  });
  return userName;
}
function fullnamestatus(val) {
  var fullname = null;
  if (val == 'not_complied') {
    fullname = 'Not Complied';
  } else if (val == 'inprogress') {
    fullname = 'Inprogress';
  } else if (val == 'delayed') {
    fullname = 'Delayed';
  } else if (val == 'complied') {
    fullname = 'Complied';
  }
  return fullname;
}
function listingCompliance(data, userid, year) {
  Custombox.close();
  totalRecordAssignee = data.total_count;


  if (snoAssignee == 0) {
  }
  var fullStatus = '';
  var statuswiselist = data.assignee_wise_drill_down;
  $.each(statuswiselist, function (ke, valu) {
    if (Object.keys(valu).length > 0) {
      ACCORDIONCOUNT = 0;
      fullStatus = fullnamestatus(ke);
      if (lastStatus != fullStatus) {
        ACCORDIONCOUNT++;
        // var tableRow = $('#templates .compliance-details-list .comp-list-statusheading');
        // var clone = tableRow.clone();
        // $('.comp-list-status a', clone).html(fullStatus);
        // $('.div-assignee-wise-compliance').append(clone);
        var tableRowheading = $('#templates .assignee-wise-accordian-list');
        var cloneHeading = tableRowheading.clone();
        $('.panel-title a', cloneHeading).text(fullStatus);
         $('.panel-title a', cloneHeading).attr('href', '#collapse' + ACCORDIONCOUNT);
        $('.panel-title a', cloneHeading).attr('aria-controls', 'collapse' + ACCORDIONCOUNT);
        if (ACCORDIONCOUNT == 1) { //For First group open collapse
            $('.panel-title a', cloneHeading).attr('aria-expanded', true);
            $('.panel-title a', cloneHeading).removeClass('collapsed');
            $(".collapse", cloneHeading).attr('id', 'collapse'+ACCORDIONCOUNT);
            $(".collapse", cloneHeading).attr('aria-labelledb', 'heading'+ACCORDIONCOUNT);
            $('.coll-title', cloneHeading).addClass('in');
        }
        $('.div-assignee-wise-compliance').append(cloneHeading);
        lastStatus = fullStatus;
      }
    }
    var list = valu;
    $.each(list, function (k, val) {
      if (lastAct != k) {
        var tableRowLevel1 = $('#templates .compliance-details-list .comp-list-level1');
        var cloneLevel1 = tableRowLevel1.clone();
        $('.comp-list-level1-val', cloneLevel1).text(k);
        $('#collapse'+ACCORDIONCOUNT+ ' .tbody-compliance-details').append(cloneLevel1);
        lastAct = k;
      }
      $.each(val, function (k2, v2) {
        var tableRowvalues = $('#templates .compliance-details-list .comp-list-tablerowlist');
        var cloneval = tableRowvalues.clone();
        snoAssignee++;
        var cDate = '';
        if (v2.completion_date != null)
          cDate = v2.completion_date;
        $('.comp-list-sno', cloneval).text(snoAssignee);
        $('.comp-list-compliance', cloneval).html(v2.compliance_name);
        $('.comp-list-startdate', cloneval).text(v2.assigned_date);
        $('.comp-list-duedate', cloneval).text(v2.due_date);
        $('.comp-list-completiondate', cloneval).text(cDate);
        $('#collapse'+ACCORDIONCOUNT+' .tbody-compliance-details').append(cloneval);
      });
    });
  });
  if (totalRecordAssignee == 0) {
    $('#pagination-assignee').hide();
    $('.compliance_count_assignee').text('');
  } else {
    $('.compliance_count_assignee').text('Showing ' + 1 + ' to ' + snoAssignee + ' of ' + totalRecordAssignee);
    if (snoAssignee >= totalRecordAssignee) {
      $('#pagination-assignee').hide();
    } else {
      $('#pagination-assignee').show();
    }
  }
}
function showPopup(country_assignee, unit_assignee, user_assignee, name_assignee) {
  $('.tbody-popup-list tr').remove();
  // $('.popupoverlay').css('visibility', 'visible');
  // $('.popupoverlay').css('opacity', '1');
  $('.year-heading').text(name_assignee);
  window.scrollTo(0, 0);
  var popupsno = 0;
  legalEntityIds = chartInput.getLegalEntities();
  client_mirror.getAssigneewiseYearwiseComplianes(country_assignee, unit_assignee, user_assignee, legalEntityIds, function (error, response) {
    if (error == null) {
      if (popupsno == 0) {
        var yearWiseDetails = response.year_wise_data;
        $.each(yearWiseDetails, function (k, val) {
          var tableRow = $('#templates .year-wise-compliance-list-popup .tablerow');
          var cloneval = tableRow.clone();
          popupsno = popupsno + 1;
          $('.popup-sno', cloneval).text(popupsno);
          $('.popup-year-val', cloneval).html(val.year);
          $('.popup-total-count', cloneval).html(val.total_compliances);
          $('.popup-complied-count', cloneval).html(val.complied_count);
          $('.popup-delayed-count', cloneval).html(val.delayed_compliance);
          $('.popup-inprogress-count', cloneval).html(val.inprogress_compliance_count);
          $('.popup-not-complied-count', cloneval).html(val.not_complied_count);
          $('.popup-click-drilldown', cloneval).on('click', function () {
            updateComplianceList(country_assignee, user_assignee, 1, parseInt(val.year), unit_assignee, 0, name_assignee, null);
          });
          $('.tbody-popup-list').append(cloneval);
        });
      }
    } else {
      console.log(error);
    }
  });
  $('.close').click(function () {
    // $('.popupoverlay').css('visibility', 'hidden');
    // $('.popupoverlay').css('opacity', '0');
    Custombox.close();
  });
}
function showPopupCompDelayed(country_id, unit_id, user_id, domain_id, name_assignee) {
  $('.tbody-popup-reassigned-list tr').remove();
  // $('.popupoverlay1').css('visibility', 'visible');
  // $('.popupoverlay1').css('opacity', '1');
  $('.comp-delayed-heading').text(name_assignee);
  window.scrollTo(0, 0);
  var popupdelayedsno = 0;
  client_mirror.getAssigneewiseReassignedComplianes(country_id, unit_id, user_id, domain_id, function (error, response) {
    if (error == null) {
      if (popupdelayedsno == 0) {
        var reassignedlist = response.chart_data;
        $.each(reassignedlist, function (k, val) {
          //alert('k')
          var tableRow = $('#templates .comp-list-delayed-row-list');
          var cloneval = tableRow.clone();
          popupdelayedsno = popupdelayedsno + 1;
          $('.comp-delayed-sno', cloneval).text(popupdelayedsno);
          $('.comp-delayed-compliance', cloneval).html(val.compliance_name);
          $('.comp-delayed-reassigned-from', cloneval).html(val.reassigned_from);
          $('.comp-delayed-startdate', cloneval).html(val.start_date);
          $('.comp-delayed-duedate', cloneval).html(val.due_date);
          $('.comp-delayed-reassigned-date', cloneval).html(val.reassigned_date);
          $('.comp-delayed-completed-date', cloneval).html(val.completed_date);
          $('.tbody-popup-reassigned-list').append(cloneval);
        });
      }
    } else {
      console.log(error);
    }
  });
  $('.close').click(function () {
    // $('.popupoverlay1').css('visibility', 'hidden');
    // $('.popupoverlay1').css('opacity', '0');
    Custombox.close();
  });
}
//drilldown load function
function loadComplianceStatusDrillDown(compliance_status, filter_type_id, filter_type_name) {
  $('#pagination').show();
  $('.table-drilldown-list thead').empty();
  $('.table-drilldown-list tbody').remove();
  $('.btn-bar-chart').hide();
  $('.btn-pie-chart').hide();
  CS_STATUS = null;
  CS_FILTERTYPEID = null;
  CS_FILTERTYPENAME = null;
  CS_LAST_UNITNAME = null;
  CS_LAST_LEVEL1 = null;
  var filter_type = chartInput.getFilterType();
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  CS_STATUS = compliance_status;
  CS_FILTERTYPEID = filter_type_id;
  CS_FILTERTYPENAME = filterType;
  SNO = 0;
  ACCORDIONCOUNT = 0;
  var legalEntityIds = chartInput.getLegalEntities();
  if (chartInput.getChartYear() == 0)
    year = chartInput.getCurrentYear();
  else
    year = chartInput.getChartYear();
  requestData = {
    'd_ids': chartInput.getDomains(),
    'from_date': chartInput.getFromDate(),
    'to_date': chartInput.getToDate(),
    'filter_type': filterType,
    'filter_id': filter_type_id,
    'compliance_status': compliance_status,
    'chart_year': year,
    'record_count': SNO,
    'le_ids': legalEntityIds
  };
  $('.btn-back').on('click', function () {
    loadComplianceStatusChart();
  });
  client_mirror.getComplianceStatusDrillDown(requestData, function (status, data) {
    COMPLIANCE_STATUS_DRILL_DOWN_DATE = data;
    updateDrillDown(compliance_status, data, filter_type_name);
  });
}
function loadEscalationDrillDown(year) {
  SNO = 0;
  ES_YEAR = year;
  ES_STATUS = null;
  ES_STATUS1 = null;
  ES_NC_UNITNAME = null;
  ES_NC_LEVEL1 = null;
  ES_NC_COUNT = 1;
  ACCORDIONCOUNTNC = 0;
  ES_D_UNITNAME = null;
  ES_D_LEVEL1 = null;
  ES_D_COUNT = 1;
  ACCORDIONCOUNTD = 0;
  $('#pagination').show();
  var filter_type = chartInput.getFilterType();
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  if (filterType == 'Group') {
    filter_ids = chartInput.getCountries();
  } else {
    filter_ids = getFilterIds(filter_type);
  }
  var legalEntityIds = chartInput.getLegalEntities();
  var requestData = {
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids,
    'chart_year': parseInt(year),
    'record_count': 0,
    'le_ids': legalEntityIds

  };
  $('.btn-back').on('click', function () {
    loadEscalationChart();
  });
  client_mirror.getEscalationDrillDown(requestData, function (status, data) {
    ESCALATION_STATUS_DRILL_DOWN_DATA = data;
    updateEscalationDrillDown(data, year);
    chartInput.setEscalationYearDrilldown = year;
  });
}
function loadTrendChartDrillDown(year) {
  SNO = 0;
  chartInput.chartYear = year;
  var filter_type = chartInput.getFilterType();
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  var requestData = {
    'c_ids': chartInput.getCountries(),
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': [1],
    'year': year,
    'record_count': SNO,
    'le_ids': chartInput.getLegalEntities()
  };
  $('.btn-back').on('click', function () {
     $('.chart-container').show();
     $('.div-drilldown-container').hide();
     loadTrendChart();
  });
  client_mirror.getTrendChartDrillDown(requestData, function (status, data) {
    TREND_CHART_DATA = data;
    updateTrendChartDrillDown(status, data, year);
  });
}
function loadNotCompliedDrillDown(type) {
  SNO = 0;
  NC_TYPE = null;
  NC_UNITNAME = null;
  NC_LEVEL1 = null;
  NC_TYPE = type;
  ACCORDIONCOUNT = 0;
  var filter_type = chartInput.getFilterType();
  var filter_ids = getFilterIds(filter_type);
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  if (filterType == 'Group') {
    filter_ids = chartInput.getCountries();
  }
  var requestData = {
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids,
    'not_complied_type': type,
    'record_count': SNO,
    'le_ids': chartInput.getLegalEntities()
  };
  client_mirror.getNotCompliedDrillDown(requestData, function (status, data) {
    NOT_COMPLIED_DRILL_DOWN_DATA = data;
    updateNotCompliedDrillDown(status, data);
  });
}
function loadComplianceApplicabilityDrillDown(type) {
  CAS_TYPE = null;
  CAS_LEVEL1 = null;
  CAS_UNITNAME = null;
  SNO = 0;
  $('#pagination').show();
  var filter_type = chartInput.getFilterType();
  filter_ids = getFilterIds(filter_type);
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  if (filterType == 'Group') {
    filter_ids = chartInput.getCountries();
  }
  var requestData = {
    'c_ids': chartInput.getCountries(),
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids,
    'applicability_status': type,
    'record_count': SNO,
    'le_ids': chartInput.getLegalEntities()
  };
  CAS_TYPE = type;
  $('.btn-back').on('click', function () {
    $('.chart-container').show();
    $('.div-drilldown-container').hide();
    loadComplianceApplicabilityChart();
  });
  client_mirror.getComplianceApplicabilityDrillDown(requestData, function (status, data) {
    COMPLIANCE_APPLICABILITY_DRILL_DOWN = data;
    updateComplianceApplicabilityDrillDown(status, data, type);
  });
}
//
// initialize
//
function initializeChartTabs() {
  $('.chart-tab').on('click', function () {
    $('.chart-filter').prop('checked', false);
    $('.filtertable .selections').hide();
    $('.btn-group').prop('checked', true);
    chartInput.setFilterType('group');
    $('.chart-tab').removeClass('active');

    if ($(this).hasClass('compliance-status-tab')) {
      $('.chart-tab.compliance-status-tab').addClass('active');
      chartInput.setChartType('compliance_status');
      loadSubFilters(selectall = true, singleSelect = "multiple");
    } else if ($(this).hasClass('escalations-tab')) {
      $('.chart-tab.escalations-tab').addClass('active');
      chartInput.setChartType('escalations');
      loadSubFilters(selectall = false, singleSelect = "");
    } else if ($(this).hasClass('not-complied-tab')) {
      $('.chart-tab.not-complied-tab').addClass('active');
      chartInput.setChartType('not_complied');
      loadSubFilters(selectall = false, singleSelect = "");
    } else if ($(this).hasClass('compliance-report-tab')) {
      $('.chart-tab.compliance-report-tab').addClass('active');
      chartInput.setChartType('compliance_report');
    } else if ($(this).hasClass('trend-chart-tab')) {
      $('.chart-tab.trend-chart-tab').addClass('active');
      chartInput.setChartType('trend_chart');
      loadSubFilters(selectall = false, singleSelect = "");
    } else if ($(this).hasClass('applicability-status-tab')) {
      $('.chart-tab.applicability-status-tab').addClass('active');
      chartInput.setChartType('applicability_status');
      loadSubFilters(selectall = false, singleSelect = "");
    }
    loadCharts();
  });
}
function initializeCharts() {
  initializeFilters();
  initializeChartTabs();
  //From Widget Url to load charts
  var wid_to_dash_url = window.sessionStorage.widget_to_dashboard_href;
  console.log("wid_to_dash_url--"+wid_to_dash_url);
  if (wid_to_dash_url != null && wid_to_dash_url != undefined && wid_to_dash_url != 'undefined') {
    $(".chart-tab").removeClass("active");
    if (wid_to_dash_url == "Compliance Status") {
      $('.chart-tab.compliance-status-tab').addClass('active');
      chartInput.setChartType('compliance_status');
      loadSubFilters(selectall = true, singleSelect = "multiple");
    } else if (wid_to_dash_url == "Escalations") {
      $('.chart-tab.escalations-tab').addClass('active');
      chartInput.setChartType('escalations');
      loadSubFilters(selectall = false, singleSelect = "");
    } else if (wid_to_dash_url == "Not Complied") {
      $('.chart-tab.not-complied-tab').addClass('active');
      chartInput.setChartType('not_complied');
      loadSubFilters(selectall = false, singleSelect = "");
    } else if (wid_to_dash_url == "Trend Chart") {
      $('.chart-tab.trend-chart-tab').addClass('active');
      chartInput.setChartType('trend_chart');
      loadSubFilters(selectall = false, singleSelect = "");
    } else if (wid_to_dash_url == "Risk Chart") {
      $('.chart-tab.applicability-status-tab').addClass('active');
      chartInput.setChartType('applicability_status');
      loadSubFilters(selectall = false, singleSelect = "");
    }
    loadCharts();
    delete window.sessionStorage.widget_to_dashboard_href;
  }
}
function toDict(target, list, id_key, value_key) {
  //console.log(list);
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    target[item[id_key]] = item[value_key];
  }
}
$(document).ready(function () {
  hideLoader();
  if (!client_mirror.verifyLoggedIn()) {
    hideLoader();
    // window.location.href = "/login";
    return;
  }
  client_mirror.getChartFilters(function (status, data) {
    if (data == null) {
      return;
    }
    CHART_FILTERS_DATA = data;
    toDict(COUNTRIES, data.countries, 'c_id', 'c_name');
    toDict(DOMAINS, data.d_info, 'd_id', 'd_name');
    toDict(BUSINESS_GROUPS, data.bg_groups, 'bg_id', 'bg_name');
    toDict(LEGAL_ENTITIES, data.le_did_infos, 'le_id', 'le_name');
    toDict(DIVISIONS, data.div_infos, 'div_id', 'div_name');
    toDict(CATEGORIES, data.cat_info, 'category_id', 'category_name');
    toDict(UNITS, data.assign_units, 'u_id', 'u_name');
    DOMAIN_INFO = data.d_months;
    GROUP_NAME = data.g_name;
    initializeCharts();
    loadCharts();
    //get_notification_count();
  });
  $('#fromdate').datepicker({
    changeMonth: true,
    changeYear: true,
    numberOfMonths: 1,
    dateFormat: 'dd-M-yy',
    monthNames: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ],
    onClose: function(selectedDate) {
      $("#todate").datepicker("option", "minDate", selectedDate);
    }
  });
  $('#todate').datepicker({
    changeMonth: true,
    changeYear: true,
    numberOfMonths: 1,
    dateFormat: 'dd-M-yy',
    monthNames: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ],
    onClose: function(selectedDate) {
      $("#fromdate").datepicker("option", "maxDate", selectedDate);
    }
  });
});
