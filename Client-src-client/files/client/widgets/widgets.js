
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

//
// Compliance status
//
function updateComplianceStatusStackBarChart(data) {
  var xAxisName = data[0];
  var xAxis = data[1];
  var chartDataSeries = data[2];
  var chartTitle = data[3];
  var drilldownSeries = data[4];
  var yAxisname = [
    'Complied',
    'Delayed Compliance',
    'Inprogress',
    'Not Complied'
  ];
  var highchart;
  highchart = new Highcharts.Chart({
    chart: {
      renderTo: 'status-container',
      type: 'bar'
    },
    title: { text: chartTitle },
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      title: { text: xAxisName },
      labels: {
        style: {
          cursor: 'pointer',
          color: 'blue',
          textDecoration: 'underline'
        },
        useHTML: true,
        formatter: function () {
          return '<div id="label_' + this.value + '">' + this.value + '</div>';
        }
      },
      tooltip: { pointFormat: 'sfosdfksdfjds' }
    },
    yAxis: {
      min: 0,
      title: { text: 'Total compliances' },
      allowDecimals: false,
      reversedStacks: false
    },
    tooltip: {
      headerFormat: '<b>{point.series.name}</b>: {point.percentage:.0f}% ',
      pointFormat: '({point.y} out of {point.stackTotal})'
    },
    plotOptions: {
      series: { pointWidth: 35 },
      bar: {
        stacking: 'normal',
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          color: '#000000',
          style: {
            textShadow: null,
            color: '#000000'
          },
          format: '{point.y}'
        },
        point: {
          events: {
          }
        }
      }
    },
    colors: [
      '#A5D17A',
      '#F58835',
      '#F0F468',
      '#F32D2B'
    ],
    series: chartDataSeries
  });
  $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
    var value = this.textContent || this.innerText;
    name = value;
    data_series = drilldownSeries[name];
    var title = chartTitle + ' - ' + name;
    // updateComplianceStatusPieChart(data_series, title, 'pie', name);
    complianceDrillDown(data_series, title, name);  // setChart(value);
  });
  year = chartInput.getChartYear();
  if (year == 0) {
    year = chartInput.getCurrentYear();
  }
  domain_ids = chartInput.getDomains();
  domain_names = [];
  for (var x = 0; x < domain_ids.length; x++) {
    id = domain_ids[x];
    domain_names.push(DOMAINS[id]);
  }
  $.each(DOMAIN_INFO, function (key, value) {
    frame_title = 'Year : ' + year + '\n';
    for (var i = 0; i < value.length; i++) {
      info = value[i];
      if (domain_names.indexOf(info.domain_name) != -1) {
        frame_title += '' + info.domain_name + ' : ' + info.period_from + ' to ' + info.period_to + '\n';
      }
    }
    $('#label_' + key).attr({
      placement: 'bottom',
      title: frame_title
    });
  });  // $("#label_India").attr({placement: 'bottom', title:"HELLO India!"});
}
//
// Escalation chart
//
function updateEscalationChart(data) {
  $('.chart-container').show();
  data = prepareEscalationChartdata(data);
  xAxis = data[0];
  chartDataSeries = data[1];
  chartTitle = data[2];
  highchart = new Highcharts.Chart({
    colors: [
      '#F58835',
      '#F32D2B'
    ],
    chart: {
      type: 'column',
      renderTo: 'status-container'
    },
    title: { text: chartTitle },
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      crosshair: true
    },
    yAxis: {
      min: 0,
      title: { text: 'Total Compliances' },
      allowDecimals: false
    },
    plotOptions: {
      series: {
        pointWidth: 40,
        groupPadding: 0.4,
        pointPadding: -0,
        pointPlacement: -0
      },
      column: {
        dataLabels: {
          enabled: true,
          textShadow: null,
          format: '{point.y}'
        }
      }
    },
    series: chartDataSeries
  });
  $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
    var year = this.textContent || this.innerText;
    loadEscalationDrillDown(year);  // setChart(value);
  });
}
//
// Not complied
//
function updateNotCompliedChart(data) {
  data = prepareNotCompliedChart(data);  
  chartDataSeries = data[0];
  chartTitle = data[1];
  total = data[2];
  highchart = new Highcharts.Chart({
    colors: [
      '#FF9C80',
      '#F2746B',
      '#FB4739',
      '#DD070C'
    ],
    chart: {
      renderTo: 'status-container',
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 55
      }
    },
    title: { text: chartTitle },
    xAxis: { categories: true },
    credits: { enabled: false },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span>{point.name} days</span>: <b>{point.y:.0f}</b> out of ' + total
    },
    legend: { enabled: true },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 35,
        dataLabels: {
          enabled: true,
          format: '{point.percentage: .0f}%'
        },
        showInLegend: true,
        point: {
          events: {            
          }
        }
      }
    },
    series: [{
        name: 'compliance',
        colorByPoint: true,
        data: chartDataSeries
      }]
  });
}
//
// Trend  chart
//
function updateTrendChart(data) {
  data = prepareTrendChartData(data);
  print_data = JSON.stringify(data, null, ' ');
  xAxis = data[0];
  chartTitle = data[1];
  chartDataSeries = data[2];
  var highchart;
  highchart = new Highcharts.Chart({
    chart: { renderTo: 'status-container' },
    title: { text: chartTitle },
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      title: { text: 'Year' },
      labels: {
        style: {
          cursor: 'pointer',
          color: 'blue',
          textDecoration: 'underline'
        }
      }
    },
    yAxis: {
      min: 0,
      title: { text: 'Compliance (%)' },
      labels: {
        formatter: function () {
          return this.value + '%';
        }
      },
      allowDecimals: false
    },
    tooltip: {
      crosshair: true,
      shared: true,
      backgroundColor: '#FCFFC5',
      headerFormat: '<b>{point.x}</b>: {point.percentage:.0f}% ',
      pointFormat: '({point.point.y} out of {point.stackTotal})',
      formatter: function () {
        var s = '<b>' + this.x + '</b>', sum = 0;
        $.each(this.points, function (i, point) {
          total = point.point.t;
          tasks = Math.round(point.point.y * 100 / total, 2);
          color = point.color;
          s += '<br/><span style="color:' + color + '"> <b>' + point.series.name + '</b> </span>: ' + tasks + '% (' + point.point.y + ' out of ' + total + ')';
          sum += point.y;
        });
        return s;
      }
    },
    plotOptions: {
      spline: {
        marker: {
          radius: 4,
          lineColor: '#666666',
          lineWidth: 1
        }
      }
    },
    series: chartDataSeries
  });
  $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
    var value = this.textContent || this.innerText;
    name = value;
    loadTrendChartDrillDown(value);
    $('.btn-back').show();
    $('.btn-back').on('click', function () {
      // updateTrendChart(data);
      loadTrendChart();
      $('.btn-back').hide();
    });  // setChart(value);
  });
}
//
// Compliance applicability status
//
function updateComplianceApplicabilityChart(data) {
  data = prepareComplianceApplicability(data);
  chartTitle = data[1];
  chartDataSeries = data[0];
  total = data[2];
  highchart = new Highcharts.Chart({
    colors: [
      '#66FF66',
      '#FFDC52',
      '#CE253C'
    ],
    chart: {
      type: 'pie',
      renderTo: 'status-container',
      options3d: {
        enabled: true,
        alpha: 55
      }
    },
    title: { text: chartTitle },
    xAxis: { categories: true },
    credits: { enabled: false },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f}</b> out of ' + total
    },
    legend: { enabled: true },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 35,
        dataLabels: {
          enabled: true,
          format: '{point.percentage: .0f}%'
        },
        showInLegend: true,
        point: {
          events: {
            click: function () {
              var drilldown = this.drilldown;
              loadComplianceApplicabilityDrillDown(drilldown);
            }
          }
        }
      }
    },
    series: [{
        name: 'compliance',
        colorByPoint: true,
        data: chartDataSeries
      }]
  });
}
//
// chartInput
//
function ChartInput() {
  this.chart_type = 'compliance_status';
  // Possiblities: "compliance_status", "escalations", "not_complied", "compliance_report", "trend_chart", "applicability_status"
  this.country_selected = false;
  this.countries = [];
  this.domain_selected = false;
  this.domains = [];
  this.date_selected = false;
  this.from_date = '';
  this.to_date = '';
  this.filter_type = 'group';
  // Possibilities: "group", "business_group", "legal_entity", "division", "unit", "consolidated"
  this.business_groups = [];
  this.legal_entities = [];
  this.divisions = [];
  this.units = [];
  this.chart_year = 0;
  // previous_year = 1, current_year = 0, next_year = -1
  this.current_year = new Date().getFullYear();
  this.range_index = 7;
  this.escalation_year = 0;
  this.setChartType = function (v) {
    this.chart_type = v;
  };
  this.getChartType = function () {
    return this.chart_type;
  };
  this.setCountrySelected = function (v) {
    this.country_selected = v;
  };
  this.setCountries = function (country_id, isAdd) {
    country_id = parseInt(country_id);
    index = this.countries.indexOf(country_id);
    if (index >= 0 && !isAdd) {
      this.countries.splice(index, 1);
      return;
    }
    if (isAdd) {
      this.countries.push(country_id);
    }
  };
  this.setCountriesAll = function (countries) {
    this.countries = copyArray(countries);
  };
  this.getCountries = function () {
    if (this.country_selected) {
      if (this.countries.length > 0)
        return copyArray(this.countries);
      else
        return [];
    } else {
      get_ids(CHART_FILTERS_DATA.countries, 'c_id');
      countries = get_ids(CHART_FILTERS_DATA.countries, 'c_id');
      chartInput.setCountriesAll(countries);
      return countries;
    }
  };
  this.setDomainSelected = function (v) {
    this.domain_selected = v;
  };
  this.setDomains = function (domain_id, isAdd) {
    domain_id = parseInt(domain_id);
    index = this.domains.indexOf(domain_id);
    if (index >= 0 && !isAdd) {
      this.domains.splice(index, 1);
      return;
    }
    if (isAdd) {
      this.domains.push(domain_id);
    }
  };
  this.setDomainsAll = function (domains) {
    this.domains = copyArray(domains);
  };
  this.getDomains = function () {
    if (this.domain_selected) {
      if (this.domains.length > 0)
        return copyArray(this.domains);
      else
        return [];
    } else {
      domains = get_ids(CHART_FILTERS_DATA.d_info, 'd_id');
      chartInput.setDomainsAll(domains);
      return domains;
    }
  };
  this.setDateSelected = function (v) {
    this.date_selected = v;
  };
  this.setFromDate = function (v) {
    this.from_date = v;
  };
  this.getFromDate = function () {
    if (this.date_selected)
      return this.from_date;
    else
      return null;
  };
  this.setToDate = function (v) {
    this.to_date = v;
  };
  this.getToDate = function () {
    if (this.date_selected)
      return this.to_date;
    else
      return null;
  };
  this.setFilterType = function (v) {
    this.filter_type = v;
  };
  this.getFilterType = function () {
    return this.filter_type;
  };
  this.setBusinessGroups = function (v, isAdd, isSingle) {
    v = parseInt(v);
    index = this.business_groups.indexOf(v);
    if (index >= 0 && !isAdd) {
      this.business_groups.splice(index, 1);
      return;
    }
    if (isSingle) {
      this.business_groups = [v];
    } else {
      if (isAdd) {
        this.business_groups.push(v);
      }
    }
  };
  this.setBusinessGroupsAll = function (business_groups) {
    this.business_groups = copyArray(business_groups);
  };
  this.getBusinessGroups = function () {
    if (this.business_groups.length > 0)
      return copyArray(this.business_groups);
    else {
      if (this.filter_type == 'business_group') {
        ids = get_ids(CHART_FILTERS_DATA.bg_groups, 'bg_id');
        if (this.chart_type == 'compliance_status')
          return ids;
        else
          return [ids[0]];
      } else
        return [];
    }
  };
  this.setLegalEntities = function (v, isAdd, isSingle) {
    v = parseInt(v);
    index = this.legal_entities.indexOf(v);
    if (index >= 0 && !isAdd) {
      this.legal_entities.splice(index, 1);
      return;
    }
    if (isSingle) {
      this.legal_entities = [v];
    } else {
      if (isAdd) {
        this.legal_entities.push(v);
      }
    }
  };
  this.setLegalEntitiesAll = function (legal_entities) {
    this.legal_entities = copyArray(legal_entities);
  };
  this.getLegalEntity = function () {
    var selectedLegalentity = client_mirror.getSelectedLegalEntity();
    return selectedLegalentity[0]['le_id'];
  };
  this.getLegalEntities = function () {
    leids = client_mirror.getSelectedLegalEntity();
    this.legal_entities = $.map(leids, function(element,index) {return element.le_id});
    if (this.legal_entities.length > 0)
      return copyArray(this.legal_entities);
    else {
      if (this.filter_type == 'legal_entity') {
        ids = get_ids(CHART_FILTERS_DATA.le_did_infos, 'le_id');
        if (this.chart_type == 'compliance_status')
          return ids;
        else
          return [ids[0]];
      } else
        return [];
    }
  };
  this.setDivisions = function (v, isAdd, isSingle) {
    v = parseInt(v);
    index = this.divisions.indexOf(v);
    if (index >= 0 && !isAdd) {
      this.divisions.splice(index, 1);
      return;
    }
    if (isSingle) {
      this.divisions = [v];
    } else {
      if (isAdd) {
        this.divisions.push(v);
      }
    }
  };
  this.setDivisionsAll = function (divisions) {
    this.divisions = copyArray(divisions);
  };
  this.getDivisions = function () {
    if (this.divisions.length > 0)
      return copyArray(this.divisions);
    else {
      if (this.filter_type == 'division') {
        ids = get_ids(CHART_FILTERS_DATA.div_infos, 'div_id');
        if (this.chart_type == 'compliance_status')
          return ids;
        else
          return [ids[0]];
      } else
        return [];
    }
  };
  this.setCategory = function (v, isAdd, isSingle) {
    v = parseInt(v);
    index = this.categories.indexOf(v);
    if (index >= 0 && !isAdd) {
      this.categories.splice(index, 1);
      return;
    }
    if (isSingle) {
      this.categories = [v];
    } else {
      if (isAdd) {
        this.categories.push(v);
      }
    }
  };
  this.setCategoryAll = function (categories) {
    this.categories = copyArray(categories);
  };
  this.getCategories = function () {
    if (this.categories.length > 0)
      return copyArray(this.categories);
    else {
      if (this.filter_type == 'category') {
        ids = get_ids(CHART_FILTERS_DATA.cat_info, 'cat_id');
        if (this.chart_type == 'compliance_status')
          return ids;
        else
          return [ids[0]];
      } else
        return [];
    }
  };
  this.setUnits = function (v, isAdd, isSingle) {
    v = parseInt(v);
    index = this.units.indexOf(v);
    if (index >= 0 && !isAdd) {
      this.units.splice(index, 1);
      return;
    }
    if (isSingle) {
      this.units = [v];
    } else {
      if (isAdd) {
        this.units.push(v);
      }
    }
  };
  this.setUnitsAll = function (units) {
    this.units = copyArray(units);
  };
  this.getUnits = function () {
    if (this.units.length > 0)
      return copyArray(this.units);
    else {
      if (this.filter_type == 'unit') {
        ids = get_ids(CHART_FILTERS_DATA.assign_units, 'u_id');
        if (this.chart_type == 'compliance_status')
          return ids;
        else
          return [ids[0]];
      } else
        return [];
    }
  };
  this.setChartYear = function (v) {
    this.chart_year = v;
  };
  this.getChartYear = function () {
    return this.chart_year;
  };
  this.setCurrentYear = function (v) {
    this.current_year = v;
  };
  this.getCurrentYear = function () {
    return this.current_year;
  };
  this.setRangeIndex = function (v) {
    this.range_index += v;
  };
  this.getRangeIndex = function () {
    return this.range_index;
  };
  this.resetRangeIndex = function () {
    this.range_index = 7;
  };
  this.setEscalationYearDrilldown = function (v) {
    this.escalation_year = v;
  };
  this.getEscalationYearDrilldown = function () {
    return this.escalation_year;
  };
}
function clearMessage() {
  $('.chart-error-message').text('');
}
function displayMessage(message) {
  $('.chart-error-message').text(message);
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function displayLoader() {
  $('.loading-indicator-spin').hide();
}
function getOptionElement(v, t, selected) {
  var option = $('<option></option>');
  option.val(v);
  option.text(t);
  if (selected) {
    option.attr('selected', true);
  }
  return option;
}
function get_ids(source, key) {
  var ids = [];
  for (var i = 0; i < source.length; i++) {
    var item = source[i];
    ids.push(item[key]);
  }
  return ids;
}
function copyArray(array) {
  return array.slice(0);
}

//
// Prepare chart data
//
function parseComplianceStatusApiInput() {
  var countryIds = chartInput.getCountries();
  var domainIds = chartInput.getDomains();
  // TODO: Validation of empty Country / Domain list.
  var filter_type = chartInput.getFilterType();
  var filterIds = getFilterIds(filter_type);
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  var fromDate = chartInput.getFromDate();
  var toDate = chartInput.getToDate();
  var chart_year = chartInput.getChartYear();
  if (chart_year == 0) {
    chart_year = chartInput.getCurrentYear();
  }
  var legalEntityIds = chartInput.getLegalEntities();
  var requestData = {
    'c_ids': countryIds,
    'd_ids': domainIds,
    'filter_type': filterType,
    'filter_ids': filterIds,
    'from_date': fromDate,
    'to_date': toDate,
    'chart_year': chart_year, 
    'le_ids': legalEntityIds
  };
  return requestData;
}
function prepareComplianceStatusChartData(chart_data) {
  // var currentYear = (new Date()).getFullYear();
  // var yearInput = chartInput.getCurrentYear()
  chartYear = chartInput.getChartYear();
  if (chartYear == 0)
    yearInput = chartInput.getCurrentYear();
  else {
    yearInput = chartYear;
  }
  // var yearInput = currentYear - chartInput.getChartYear();
  var chartTitle = getFilterTypeTitle();
  var domainsInput = chartInput.getDomains();
  var countriesInput = chartInput.getCountries();
  var xAxis = [];
  var xAxisIds = [];
  var yAxisComplied = [];
  var yAxisDelayed = [];
  var yAxisInprogress = [];
  var yAxisNotComplied = [];
  for (var i = 0; i < chart_data.length; i++) {
    var chartData = chart_data[i];
    var filter_type_id = chartData.filter_type_id;
    filterTypeInput = getFilterTypeInput();
    // if (!(filter_type_id in filterTypeInput))
    //     continue;
    if (filterTypeInput.indexOf(filter_type_id) == -1)
      continue;
    var filterTypeName = getFilterTypeName(filter_type_id);
    var compliedCount = 0;
    var delayedCount = 0;
    var inprogressCount = 0;
    var notCompliedCount = 0;
    for (var j = 0; j < chartData.c_data.length; j++) {
      var item = chartData.c_data[j];
      if (parseInt(item.year) != yearInput)
        continue;
      compliedCount += item.complied_count;
      delayedCount += item.delayed_compliance_count;
      inprogressCount += item.inprogress_compliance_count;
      notCompliedCount += item.not_complied_count;
    }
    ;
    if (compliedCount == 0 && delayedCount == 0 && inprogressCount == 0 && notCompliedCount == 0) {
      continue;
    }
    xAxis.push(filterTypeName);
    xAxisIds.push(filter_type_id);
    yAxisComplied.push(compliedCount);
    yAxisDelayed.push(delayedCount);
    yAxisInprogress.push(inprogressCount);
    yAxisNotComplied.push(notCompliedCount);
  }
  // if (xAxis.length == 0)
  //     return null;
  var xAxisName = getXAxisName();
  var yAxis = [
    'Complied',
    'Delayed Compliance',
    'Inprogress',
    'Not Complied'
  ];
  var yAxisData = [
    yAxisComplied,
    yAxisDelayed,
    yAxisInprogress,
    yAxisNotComplied
  ];
  function sum_values(arr) {
    var sum = arr.reduce(function (pv, cv) {
      return pv + cv;
    }, 0);
    return sum;
  }
  if (chartTitle == 'Consolidated') {
    data_series = [];
    for (var i = 0; i < yAxis.length; i++) {
      if (sum_values(yAxisData[i]) == 0)
        v_visible = false;
      else
        v_visible = true;
      data_series.push({
        'name': yAxis[i],
        'y': sum_values(yAxisData[i]),
        'visible': v_visible
      });
    }
    return data_series;
  }
  var chartDataSeries = [];
  for (var i = 0; i < yAxis.length; i++) {
    values = yAxisData[i];
    y_list = [];
    for (var x = 0; x < values.length; x++) {
      if (values[x] == 0)
        v_visible = false;
      else
        v_visible = true;
      y_list.push({
        'y': values[x],
        'drilldown': yAxis[i],
        'filter_type_id': xAxisIds[x],
        'visible': v_visible
      });
    }
    chartDataSeries.push({
      'name': yAxis[i],
      'data': y_list
    });
  }
  var xAxisDrillDownSeries = {};
  for (var j = 0; j < xAxis.length; j++) {
    data_list = [];
    for (var x1 = 0; x1 < yAxis.length; x1++) {
      value = yAxisData[x1][j];
      if (value == 0)
        v_visible = false;
      else
        v_visible = true;
      data_list.push({
        'name': yAxis[x1],
        'y': value,
        'filter_id': xAxisIds[j],
        'drilldown': xAxis[j],
        'visible': v_visible
      });
    }
    xAxisDrillDownSeries[xAxis[j]] = data_list;
  }
  chartTitle = chartTitle + ' wise compliances';
  return [
    xAxisName,
    xAxis,
    chartDataSeries,
    chartTitle,
    xAxisDrillDownSeries
  ];
}
// Escalation
function prepareEscalationChartdata(source_data) {  
  var chartTitle = getFilterTypeTitle();
  var xAxis = [];
  function set_value(dict, key, value) {
    var temp = dict[key];
    if (typeof temp === 'undefined')
      temp = 0;
    temp = parseInt(temp) + parseInt(value);
    dict[key] = temp;
  }
  chart_data = source_data.es_chart_data;
  var chartDataSeries = [];
  delayed_data = [];
  not_complied_data = [];
  $.each(chart_data, function (i, value) {
    delayed = value.delayed_compliance_count;
    not_complied = value.not_complied_count;
    year = value.chart_year;
    if (delayed == 0 && not_complied == 0) {
    } else {
      if (delayed == 0)
        v_visible = false;
      else
        v_visible = true;
      delayed_data.push({
        'y': delayed,
        'drilldown': 'Delayed Compliance',
        'year': year,
        'visible': v_visible
      });
      if (not_complied == 0)
        v_visible = false;
      else
        v_visible = true;
      not_complied_data.push({
        'y': not_complied,
        'drilldown': 'Not Complied',
        'year': year,
        'visible': v_visible
      });
      xAxis.push(year);
    }
  });
  chartDataSeries.push({
    'name': 'Delayed Compliance',
    'data': delayed_data
  });
  chartDataSeries.push({
    'name': 'Not Complied',
    'data': not_complied_data
  });
  var filterTypeInput = getFilterTypeInput();
  if (chartTitle == 'Country') {
    chartTitle = 'Escalation of ' + GROUP_NAME;
  } else {
    filter_names = [];
    for (var i = 0; i < filterTypeInput.length; i++) {
      name = getFilterTypeName(filterTypeInput[i]);
      filter_names.push(name);
    }
    chartTitle = 'Escalation of ' + chartTitle + ' ' + filter_names;
  }
  return [
    xAxis,
    chartDataSeries,
    chartTitle
  ];
}
// Trend Chart
function prepareTrendChartData(source_data) {
  var chartTitle = getFilterTypeTitle();
  var xAxis = [];
  var xAxisIds = [];
  var chartDataSeries = [];
  var total_count = [];

  //xAxis = source_data.years;
  for (var i = 0; i < source_data.trend_data.length; i++) {
    chartData = source_data.trend_data[i];
    var filter_type_id = chartData.filter_id;
    var filterTypeInput = getFilterTypeInput();
    if (filterTypeInput.indexOf(filter_type_id) == -1)
      continue;
    var filterTypeName = getFilterTypeName(filter_type_id);
        
    //compliance_info = chartData.complied_compliance;
    data = [];
//   for (var j = 0; j < compliance_info.length; j++) {
      //compliance_count.push(compliance_info[j].complied_compliances_count);
    total_count.push(chartData.total_compliances);
      data.push({
        y: chartData.complied_compliances_count,
        t: chartData.total_compliances
      });
    //}

    chartDataSeries.push({
      'name': filterTypeName,
      'data': data,
      'total': total_count
    });
    xAxis.push(chartData.chart_year);
  }
  chartTitle = 'Complied (' + xAxis[0] + ' to ' + xAxis[xAxis.length - 1] + ')';
  
  return [
    xAxis,
    chartTitle,
    chartDataSeries
  ];
}
function prepareNotCompliedChart(source_data) {
  var chartTitle = getFilterTypeTitle();
  var chartDataSeries = [];
  count = 0;
  $.each(source_data, function (key, item) {
    count += item;
    if (item == 0)
      v_visible = false;
    else
      v_visible = true;
    if (key == 'T_31_to_60_days_count') {
      chartDataSeries.push({
        name: 'Below 60',
        y: item,
        drilldown: 'Below 60',
        visible: v_visible
      });
    } else if (key == 'T_0_to_30_days_count') {
      chartDataSeries.push({
        name: 'Below 30',
        y: item,
        drilldown: 'Below 30',
        visible: v_visible
      });
    } else if (key == 'T_61_to_90_days_count') {
      chartDataSeries.push({
        name: 'Below 90',
        y: item,
        drilldown: 'Below 90',
        visible: v_visible
      });
    } else if (key == 'Above_90_days_count') {
      chartDataSeries.push({
        name: 'Above 90',
        y: item,
        drilldown: 'Above 90',
        visible: v_visible
      });
    }
  });
  if (count == 0)
    chartDataSeries = [];
  var filterTypeInput = getFilterTypeInput();
  if (chartTitle == 'Country') {
    chartTitle = 'Over due compliance of ' + GROUP_NAME;
  } else {
    filter_names = [];
    for (var i = 0; i < filterTypeInput.length; i++) {
      name = getFilterTypeName(filterTypeInput[i]);
      filter_names.push(name);
    }
    chartTitle = 'Over due compliance of ' + chartTitle + ' ' + filter_names;
  }
  return [
    chartDataSeries,
    chartTitle,
    count
  ];
}
function prepareComplianceApplicability(source_data) {
  chartDataSeries = [];
  chartTitle = getFilterTypeTitle();
  rejected_count = source_data.rejected_count;
  not_complied_count = source_data.not_complied_count;
  unassign_count = source_data.unassign_count;
  not_opted = source_data.not_opted_count;
  total = parseInt(rejected_count) + parseInt(not_complied_count) + parseInt(unassign_count) + parseInt(not_opted);
  if (rejected_count == 0 && not_complied_count == 0 && unassign_count == 0 && not_opted == 0) {
  } else {
    if (rejected_count == 0)
      v_visible = false;
    else
      v_visible = true;
    chartDataSeries.push({
      name: 'Rejected',
      y: rejected_count,
      drilldown: 'Rejected',
      visible: v_visible
    });
    if (not_complied_count == 0)
      v_visible = false;
    else
      v_visible = true;
    chartDataSeries.push({
      name: 'Not Complied',
      y: not_complied_count,
      drilldown: 'Not Complied',
      visible: v_visible
    });
    if (unassign_count == 0)
      v_visible = false;
    else
      v_visible = true;
    chartDataSeries.push({
      name: 'Unassigned',
      y: unassign_count,
      drilldown: 'Unassigned',
      visible: v_visible
    });
    if (not_opted == 0)
      v_visible = false;
    else
      v_visible = true;
    chartDataSeries.push({
      name: 'Not Opted',
      y: not_opted,
      drilldown: 'Not Opted',
      visible: v_visible
    });
  }
  var filterTypeInput = getFilterTypeInput();
  if (chartTitle == 'Country') {
    chartTitle = 'Risk Chart of ' + GROUP_NAME;
  } else {
    filter_names = [];
    for (var i = 0; i < filterTypeInput.length; i++) {
      name = getFilterTypeName(filterTypeInput[i]);
      filter_names.push(name);
    }
    chartTitle = 'Risk Chart of ' + chartTitle + ' ' + filter_names;
  }
  return [
    chartDataSeries,
    chartTitle,
    total
  ];
}
// Load chart
function loadComplianceStatusChart() {
  var requestData = parseComplianceStatusApiInput();
  client_mirror.getComplianceStatusChartData(requestData, function (status, data) {
    // TODO: API Error Validation
    COMPLIANCE_STATUS_DATA = data.chart_data;
    if (COMPLIANCE_STATUS_DATA.length > 7) {
      data1 = [];
      for (i = 0; i < 7; i++) {
        if (COMPLIANCE_STATUS_DATA.length > i)
          data1.push(COMPLIANCE_STATUS_DATA[i]);
      }
      updateComplianceStatusChart(data1);
    } else {
      updateComplianceStatusChart(COMPLIANCE_STATUS_DATA);
    }
    chartInput.resetRangeIndex();
    hideLoader();
    range = chartInput.getRangeIndex();
    if (COMPLIANCE_STATUS_DATA.length <= range) {
      hidePreviousNext();
    } else {
      showPreviousNext();
    }
    $('.btn-previous').hide();
  });
}
function loadEscalationChart() {
  var filter_type = chartInput.getFilterType();
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  if (filterType == 'Group') {
    filter_ids = chartInput.getCountries();
  } else {
    filter_ids = getFilterIds(filter_type);
  }
  legalEntityIds = chartInput.getLegalEntities();
  var requestData = {
    'c_ids': chartInput.getCountries(),
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids,
    'le_ids': legalEntityIds
  };
  client_mirror.getEscalationChartData(requestData, function (status, data) {
    ESCALATION_DATA = data;
    updateEscalationChart(data);
  });
}
function loadTrendChart() {
  var filter_type = chartInput.getFilterType();
  var filter_ids = getFilterIds(filter_type);
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  if (filterType == 'Group') {
    filter_ids = chartInput.getCountries();
  }
  var legalEntityIds = chartInput.getLegalEntities();
  var requestData = {
    'c_ids': chartInput.getCountries(),
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids,
    'le_ids': legalEntityIds
  };
  client_mirror.getTrendChart(requestData, function (status, data) {
    TREND_CHART_DATA = data;
    updateTrendChart(data);
  });
}
function loadNotCompliedChart() {
  var filter_type = chartInput.getFilterType();
  var filter_ids = getFilterIds(filter_type);
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  if (filterType == 'Group') {
    filter_ids = chartInput.getCountries();
  }
  var legalEntityIds = chartInput.getLegalEntities();
  var requestData = {
    'c_ids': chartInput.getCountries(),
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids,
    'le_ids': legalEntityIds
  };
  client_mirror.getNotCompliedData(requestData, function (status, data) {
    NOT_COMPLIED_DATA = data;
    updateNotCompliedChart(data);
  });
}
function loadComplianceApplicabilityChart() {
  var filter_type = chartInput.getFilterType();
  var filter_ids = getFilterIds(filter_type);
  var filter_type = chartInput.getFilterType().replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filter_type);
  if (filterType == 'Group') {
    filter_ids = chartInput.getCountries();
  }
  var requestData = {
    'c_ids': chartInput.getCountries(),
    'd_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids,
    'le_ids': chartInput.getLegalEntities()

  };
  client_mirror.getComplianceApplicabilityChart(requestData, function (status, data) {
    COMPLIANCE_APPLICABILITY_DATA = data;
    updateComplianceApplicabilityChart(data);
  });
}
function loadAssigneeWiseCompliance() {
  client_mirror.getAssigneewiseComplianesFilters(function (status, data) {
    updateAssigneeWiseComplianceFiltersList(data);
  });
}
function loadCharts() {
  // displayLoader();
  hideButtons();
  $('.drilldown-container').hide();
  $('.graph-container.compliance-status').show();
  var chartType = chartInput.getChartType();
  chartInput.setChartYear(0);
  if (chartType == 'compliance_report') {
    $('.chart-container-inner').hide();
    $('.report-container-inner').show();
  } else {
    if (chartType == 'compliance_status') {
      $('.chart-filters').show();
      $('.chart-filters-autocomplete').hide();
      $('.graph-selections-bottom').show();
      $('#DateSelection').show();
      $('.btn-consolidated').show();
    } else {
      $('.chart-filters').show();
      $('.chart-filters-autocomplete').hide();
      $('.graph-selections-bottom').hide();
      $('#DateSelection').hide();
      $('.btn-consolidated').hide();
    }
    $('.chart-container-inner').show();
    $('.report-container-inner').hide();
  }
  $(".assignee-wise").empty();
  if (chartType == 'compliance_status') {
    PageTitle.val("Compliance Status");
    loadComplianceStatusChart();
  } else if (chartType == 'escalations') {
    PageTitle.html("Escalation");
    loadEscalationChart();
  } else if (chartType == 'not_complied') {
    PageTitle.html("Not Complied");
    loadNotCompliedChart();
  } else if (chartType == 'compliance_report') {
    PageTitle.html("Assignee Wise Compliances");
    $(".drilldown-container").empty();
    loadAssigneeWiseCompliance();
  } else if (chartType == 'trend_chart') {
    PageTitle.html("Trend Chart");
    loadTrendChart();
  } else if (chartType == 'applicability_status') {
    PageTitle.html("Risk Report");
    loadComplianceApplicabilityChart();
  } else if (chartType == 'assignee_wise_compliance') {
    PageTitle.html("Assignee Wise Compliances");
    loadAssignessWiseComplianceChart();
  } else {
    hideLoader();
  }
}

function loadSidebarMenu(){
  client_mirror.

}

$(document).ready(function () {
  hideLoader();
  loadSidebarMenu();

});