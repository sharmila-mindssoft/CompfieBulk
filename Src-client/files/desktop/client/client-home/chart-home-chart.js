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
            click: function () {
              var drilldown = this.drilldown;
              if (drilldown) {
                filter_name = xAxis[this.x];
                loadComplianceStatusDrillDown(drilldown, this.filter_type_id, filter_name);
              }
            }
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
    updateComplianceStatusPieChart(data_series, title, 'pie', name);
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
function updateComplianceStatusPieChart(data_list, chartTitle, chartType, filter_name) {
  var total = 0;
  for (var i = 0; i < data_list.length; i++) {
    item = data_list[i];
    total += parseInt(item.y);
  }
  var options = {
    // var options = new Highcharts.Chart({
    colors: [
      '#A5D17A',
      '#F58835',
      '#F0F468',
      '#F32D2B'
    ],
    chart: { renderTo: 'status-container' },
    title: { text: chartTitle },
    credits: { enabled: false },
    xAxis: {
      categories: true,
      title: { text: 'Compliance Status' }
    },
    yAxis: { title: { text: 'Total compliances' } },
    tooltip: {
      headerFormat: '',
      pointFormat: '{point.name}:{point.y} Out of ' + total
    },
    legend: { enabled: true },
    plotOptions: {
      series: {
        pointWidth: 50,
        allowPointSelect: true
      },
      column: {
        colorByPoint: true,
        point: {
          events: {
            click: function () {
              var drilldown = this.drilldown;
              if (drilldown) {
                loadComplianceStatusDrillDown(this.name, this.filter_id, filter_name);
              }
            }
          }
        }
      },
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 35,
        dataLabels: {
          enabled: true,
          format: '{point.percentage:.0f}%'
        },
        showInLegend: true,
        point: {
          events: {
            click: function () {
              var drilldown = this.drilldown;
              if (drilldown) {
                loadComplianceStatusDrillDown(this.name, this.filter_id, filter_name);
              }
            }
          }
        }
      }
    },
    series: [{ data: data_list }]
  };
  $('.btn-back').show();
  if (chartType == 'pie') {
    $('.btn-pie-chart').hide();
    $('.btn-bar-chart').show();
    options.chart.type = 'pie';
    options.chart.options3d = {
      enabled: true,
      alpha: 55,
      beta: 0
    };
    var chart1 = new Highcharts.Chart(options);
  } else {
    $('.btn-pie-chart').show();
    $('.btn-bar-chart').hide();
    options.chart.type = 'column';
    options.legend.enabled = false;
    options.colors = [
      '#A5D17A',
      '#F58835',
      '#F0F468',
      '#F32D2B'
    ];
    var chart1 = new Highcharts.Chart(options);
  }
}
//
// Escalation chart
//
function updateEscalationChart(data) {
  $('.graph-container.compliance-status').show();
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
            click: function () {
              var drilldown = this.drilldown;
              loadNotCompliedDrillDown(drilldown);
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
      pointFormat: '({point.y} out of {point.stackTotal})',
      formatter: function () {
        var s = '<b>' + this.x + '</b>', sum = 0;
        $.each(this.points, function (i, point) {
          total = point.point.t;
          tasks = point.y / 100 * total;
          color = point.color;
          s += '<br/><span style="color:' + color + '"> <b>' + point.series.name + '</b> </span>: ' + point.y + '% (' + Math.round(tasks) + ' out of ' + total + ')';
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
      updateTrendChart(data);
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
      get_ids(CHART_FILTERS_DATA.countries, 'country_id');
      countries = get_ids(CHART_FILTERS_DATA.countries, 'country_id');
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
      domains = get_ids(CHART_FILTERS_DATA.domains, 'domain_id');
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
        ids = get_ids(CHART_FILTERS_DATA.business_groups, 'business_group_id');
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
  this.getLegalEntities = function () {
    if (this.legal_entities.length > 0)
      return copyArray(this.legal_entities);
    else {
      if (this.filter_type == 'legal_entity') {
        ids = get_ids(CHART_FILTERS_DATA.legal_entities, 'legal_entity_id');
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
        ids = get_ids(CHART_FILTERS_DATA.divisions, 'division_id');
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
        ids = get_ids(CHART_FILTERS_DATA.units, 'unit_id');
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
function getFilterIds(filter_type) {
  var filterIds = null;
  if (filter_type.trim() == 'business_group') {
    filterIds = chartInput.getBusinessGroups();
  } else if (filter_type == 'legal_entity')
    filterIds = chartInput.getLegalEntities();
  else if (filter_type == 'division')
    filterIds = chartInput.getDivisions();
  else if (filter_type == 'unit')
    filterIds = chartInput.getUnits();
  return filterIds;
}
function getFilterTypeInput() {
  if (chartInput.filter_type == 'group' || chartInput.filter_type == 'consolidated') {
    return chartInput.getCountries();
  } else if (chartInput.filter_type == 'business_group') {
    return chartInput.getBusinessGroups();
  } else if (chartInput.filter_type == 'legal_entity') {
    return chartInput.getLegalEntities();
  } else if (chartInput.filter_type == 'division') {
    return chartInput.getDivisions();
  } else if (chartInput.filter_type == 'unit') {
    return chartInput.getUnits();
  } else {
    return null;
  }
}
function getFilterTypeName(filter_type_id) {
  if (chartInput.filter_type == 'group') {
    return COUNTRIES[filter_type_id];
  } else if (chartInput.filter_type == 'business_group') {
    return BUSINESS_GROUPS[filter_type_id];
  } else if (chartInput.filter_type == 'legal_entity') {
    return LEGAL_ENTITIES[filter_type_id];
  } else if (chartInput.filter_type == 'division') {
    return DIVISIONS[filter_type_id];
  } else if (chartInput.filter_type == 'unit') {
    return UNITS[filter_type_id];
  } else {
    return null;
  }
}
function getFilterTypeTitle() {
  if (chartInput.filter_type == 'group') {
    return 'Country';
  } else if (chartInput.filter_type == 'business_group') {
    return 'Business Group';
  } else if (chartInput.filter_type == 'legal_entity') {
    return 'Legal Entity';
  } else if (chartInput.filter_type == 'division') {
    return 'Division';
  } else if (chartInput.filter_type == 'unit') {
    return 'Unit';
  } else if (chartInput.filter_type == 'consolidated') {
    return 'Consolidated';
  } else {
    return null;
  }
}
function getXAxisName() {
  xAxisNames = {
    'group': 'Countries',
    'business_group': 'Business Groups',
    'legal_entity': 'Legal Entities',
    'division': 'Divisions',
    'unit': 'Units'
  };
  var filterType = chartInput.getFilterType();
  return xAxisNames[filterType];
}
function hideButtons() {
  $('.btn-back').hide();
  $('.btn-pie-chart').hide();
  $('.btn-bar-chart').hide();
}
function showPreviousNext() {
  $('.btn-previous').show();
  $('.btn-next').show();
}
function hidePreviousNext() {
  $('.btn-previous').hide();
  $('.btn-next').hide();
}
//
// Load filters
//
function loadCountries() {
  countries = CHART_FILTERS_DATA.countries;
  for (var i = 0; i < countries.length; i++) {
    var country = countries[i];
    var option = getOptionElement(country.country_id, country.country_name, true);
    $('.country-filter').append(option);
  }
}
function loadDomains() {
  domains = CHART_FILTERS_DATA.domains;
  for (var i = 0; i < domains.length; i++) {
    var domain = domains[i];
    var option = getOptionElement(domain.domain_id, domain.domain_name, true);
    $('.domain-filter').append(option);
  }
}
function loadBusinessGroups(isSelectAll) {
  business_groups = CHART_FILTERS_DATA.business_groups;
  for (var i = 0; i < business_groups.length; i++) {
    var business_group = business_groups[i];
    var option = getOptionElement(business_group.business_group_id, business_group.business_group_name, isSelectAll);
    $('.bg-filter').append(option);
  }
  if (business_groups.length == 0) {
    $('.btn-business-group').hide();
  }
}
function loadLegalEntities(isSelectAll) {
  legal_entities = CHART_FILTERS_DATA.legal_entities;
  for (var i = 0; i < legal_entities.length; i++) {
    var legal_entity = legal_entities[i];
    var option = getOptionElement(legal_entity.legal_entity_id, legal_entity.legal_entity_name, isSelectAll);
    $('.legal-entity-filter').append(option);
  }
}
function loadDivisions(isSelectAll) {
  divisions = CHART_FILTERS_DATA.divisions;
  for (var i = 0; i < divisions.length; i++) {
    var division = divisions[i];
    var option = getOptionElement(division.division_id, division.division_name, isSelectAll);
    $('.division-filter').append(option);
  }
  if (divisions.length == 0) {
    $('.btn-division').hide();
  }
}
function loadUnits(isSelectAll) {
  $('.unit-filter').empty();
  units = CHART_FILTERS_DATA.units;
  for (var i = 0; i < units.length; i++) {
    var unit = units[i];
    var option = getOptionElement(unit.unit_id, unit.unit_name, isSelectAll);
    $('.unit-filter').append(option);
  }
}
function loadSubFilters(isSelectAll, isSingleSelect) {
  loadBusinessGroups(isSelectAll);
  loadLegalEntities(isSelectAll);
  loadDivisions(isSelectAll);
  loadUnits(isSelectAll);
  $('.bg-filter').multipleSelect({
    filter: true,
    selectAll: isSelectAll,
    single: isSingleSelect,
    placeholder: 'Select Business Group',
    onClick: function (business_group) {
      chartInput.setBusinessGroups(business_group.value, business_group.checked, isSingleSelect);
    },
    onCheckAll: function () {
      business_groups = get_ids(CHART_FILTERS_DATA.business_groups, 'business_group_id');
      chartInput.setBusinessGroupsAll(business_groups);
    },
    onUncheckAll: function () {
      chartInput.setBusinessGroupsAll([]);
    }
  });
  $('.legal-entity-filter').multipleSelect({
    filter: true,
    selectAll: isSelectAll,
    single: isSingleSelect,
    placeholder: 'Select Legal Entity',
    onClick: function (legal_entity) {
      chartInput.setLegalEntities(legal_entity.value, legal_entity.checked, isSingleSelect);
    },
    onCheckAll: function () {
      legal_entities = get_ids(CHART_FILTERS_DATA.legal_entities, 'legal_entity_id');
      chartInput.setLegalEntitiesAll(legal_entities);
    },
    onUncheckAll: function () {
      chartInput.setLegalEntitiesAll([]);
    }
  });
  $('.division-filter').multipleSelect({
    filter: true,
    selectAll: isSelectAll,
    single: isSingleSelect,
    placeholder: 'Select Division',
    onClick: function (division) {
      chartInput.setDivisions(division.value, division.checked, isSingleSelect);
    },
    onCheckAll: function () {
      divisions = get_ids(CHART_FILTERS_DATA.divisions, 'division_id');
      chartInput.setDivisionsAll(divisions);
    },
    onUncheckAll: function () {
      chartInput.setDivisionsAll([]);
    }
  });
  $('.unit-filter').multipleSelect({
    filter: true,
    selectAll: isSelectAll,
    single: isSingleSelect,
    placeholder: 'Select Unit',
    onClick: function (unit) {
      chartInput.setUnits(unit.value, unit.checked, isSingleSelect);
    },
    onCheckAll: function () {
      units = get_ids(CHART_FILTERS_DATA.units, 'unit_id');
      chartInput.setUnitsAll(units);
    },
    onUncheckAll: function () {
      chartInput.setUnitsAll([]);
    }
  });
}
function initializeFilters() {
  loadCountries();
  $('.country-filter').multipleSelect({
    filter: true,
    placeholder: 'Select Country',
    onClick: function (country) {
      chartInput.setCountries(country.value, country.checked);
    },
    onCheckAll: function () {
      countries = get_ids(CHART_FILTERS_DATA.countries, 'country_id');
      chartInput.setCountriesAll(countries);
    },
    onUncheckAll: function () {
      chartInput.setCountriesAll([]);
    }
  });
  loadDomains();
  $('.domain-filter').multipleSelect({
    filter: true,
    placeholder: 'Select Domain',
    onClick: function (domain) {
      chartInput.setDomains(domain.value, domain.checked);
    },
    onCheckAll: function () {
      domains = get_ids(CHART_FILTERS_DATA.domains, 'domain_id');
      chartInput.setDomainsAll(domains);
    },
    onUncheckAll: function () {
      chartInput.setDomainsAll([]);
    }
  });
  loadSubFilters(selectall = true, singleSelect = false);
  $('.btn-country').on('click', function () {
    $(this).toggleClass('active');
    if ($(this).hasClass('active')) {
      chartInput.setCountrySelected(true);
      $('.country-selection').show();
    } else {
      chartInput.setCountrySelected(false);
      $('.country-selection').hide();
    }
  });
  $('.btn-domain').on('click', function () {
    $(this).toggleClass('active');
    if ($(this).hasClass('active')) {
      chartInput.setDomainSelected(true);
      $('.domain-selection').show();
    } else {
      chartInput.setDomainSelected(false);
      $('.domain-selection').hide();
    }
  });
  $('.btn-date').on('click', function () {
    $(this).toggleClass('active');
    if ($(this).hasClass('active')) {
      chartInput.setDateSelected(true);
      $('.date-selection').show();
    } else {
      chartInput.setDateSelected(false);
      $('.date-selection').hide();
    }
  });
  $('.btn-date-filter').on('click', function () {
    var from_date = $('#fromdate').val();
    var to_date = $('#todate').val();
    if (from_date.length > 0 && to_date.length > 0) {
      chartInput.setFromDate(from_date);
      chartInput.setToDate(to_date);
      loadCharts();
    }
  });
  $('.chart-filter').on('click', function () {
    // if ($(this).hasClass("active"))
    //     return;
    var filter_type = $(this).attr('class').split(' ')[1];
    filter_type = filter_type.replace('btn-', '');
    filter_type = filter_type.replace('-', '_');
    chartInput.setFilterType(filter_type);
    $('.filtertable .selections').hide();
    if (filter_type in [
        'group',
        'consolidated'
      ])
      return;
    var filter_type_selection = filter_type.replace('_', '-') + '-selection';
    $(this).toggleClass('active');
    if ($(this).hasClass('active')) {
      $('.chart-filter').removeClass('active');
      $(this).addClass('active');
      $('.' + filter_type_selection).show();
    } else {
      $('.' + filter_type_selection).hide();
    }
    var chart_type = chartInput.getChartType();
    if (filter_type == 'group' || filter_type == 'consolidated') {
      loadCharts();
    }
  });
  $('.common-filter .btn-go input').on('click', function () {
    var chart_type = chartInput.getChartType();
    loadCharts();
  });
  $('.specific-filter .btn-go input').on('click', function () {
    loadCharts();
  });
  $('.btn-previous-year').on('click', function (event) {
    $('.btn-next-year').show();
    event.preventDefault();
    event.stopPropagation();
    currentYear = chartInput.getCurrentYear();
    chartYear = chartInput.getChartYear();
    if (chartYear == 0) {
      chartInput.setChartYear(currentYear - 1);
    } else {
      chartInput.setChartYear(chartYear - 1);
    }
    loadComplianceStatusChart();
  });
  $('.btn-next-year').on('click', function () {
    currentYear = chartInput.getCurrentYear();
    chartYear = chartInput.getChartYear();
    chartInput.setChartYear(chartYear + 1);
    loadComplianceStatusChart();
    if (chartInput.getCurrentYear() == chartInput.getChartYear()) {
      $('.btn-next-year').hide();
    }
  });
  $('.btn-next').on('click', function () {
    range = chartInput.getRangeIndex();
    var data = [];
    for (i = range; i < range + 7; i++) {
      if (COMPLIANCE_STATUS_DATA[i] !== undefined)
        data.push(COMPLIANCE_STATUS_DATA[i]);
    }
    chartInput.setRangeIndex(7);
    updateComplianceStatusChart(data);
    $('.btn-previous').show();
    if (range >= COMPLIANCE_STATUS_DATA.length) {
      alert('next hide');
      $('.btn-next').hide();
    }
  });
  $('.btn-previous').on('click', function () {
    $('.btn-next').show();
    chartInput.setRangeIndex(-7);
    range = chartInput.getRangeIndex();
    var data = [];
    for (i = range - 7; i < range; i++) {
      if (COMPLIANCE_STATUS_DATA[i] !== undefined)
        data.push(COMPLIANCE_STATUS_DATA[i]);
    }
    if (range == 7) {
      $('.btn-previous').hide();
    }
    updateComplianceStatusChart(data);
  });
}
//retrive country autocomplete value
function onCountrySuccess(val) {
  $('#countryval').val(val[1]);
  $('#country').val(val[0]);
}
//load country list in autocomplete text box
function ac_country_load(textval, e) {
  getCountryAutocomplete(e, textval, COUNTRYLIST, function (val) {
    onCountrySuccess(val);
  });
}
//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val) {
  $('#legalentityval').val(val[1]);
  $('#legalentityid').val(val[0]);
}
//load legalentity form list in autocomplete text box
function ac_le_load(textval, e) {
  getClientLegalEntityAutocomplete(e, textval, LEGALENTITYLIST, function (val) {
    onLegalEntitySuccess(val);
  });
}
//retrive unit form autocomplete value
function onUnitSuccess(val) {
  $('#unitval').val(val[1]);
  $('#unitid').val(val[0]);
}
//load unit  form list in autocomplete text box
function ac_unit_load(textval, e) {
  //var cId = $("#country").val();
  //var dId = 0;
  getUnitAutocomplete(e, textval, UNITLIST, function (val) {
    onUnitSuccess(val);
  });
}
//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val) {
  $('#businessgroupsval').val(val[1]);
  $('#businessgroupid').val(val[0]);
}
//load businessgroup form list in autocomplete text box
function ac_bg_load(textval, e) {
  getClientBusinessGroupAutocomplete(e, textval, BUSINESSGROUPSLIST, function (val) {
    onBusinessGroupSuccess(val);
  });
}
//retrive division form autocomplete value
function onDivisionSuccess(val) {
  $('#divisionval').val(val[1]);
  $('#divisionid').val(val[0]);
}
//load division form list in autocomplete text box
function ac_division_load(textval, e) {
  getClientDivisionAutocomplete(e, textval, DIVISIONLIST, function (val) {
    onDivisionSuccess(val);
  });
}
//retrive user autocomplete value
function onUserSuccess(val) {
  $('#userval').val(val[1]);
  $('#userid').val(val[0]);
}
//load user list in autocomplete text box
function ac_user_load(textval, e) {
  getUserAutocomplete(e, textval, USERLIST, function (val) {
    onUserSuccess(val);
  });
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
  var requestData = {
    'country_ids': countryIds,
    'domain_ids': domainIds,
    'filter_type': filterType,
    'filter_ids': filterIds,
    'from_date': fromDate,
    'to_date': toDate,
    'chart_year': chart_year
  };
  return requestData;
}
function prepareComplianceStatusChartData(chart_data) {
  console.log(chart_data);
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
    for (var j = 0; j < chartData.data.length; j++) {
      var item = chartData.data[j];
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
  chart_data = source_data.chart_data;
  var chartDataSeries = [];
  delayed_data = [];
  not_complied_data = [];
  $.each(chart_data, function (i, value) {
    delayed = value.delayed_compliance_count;
    not_complied = value.not_complied_count;
    year = value.year;
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
  xAxis = source_data.years;
  for (var i = 0; i < source_data.data.length; i++) {
    chartData = source_data.data[i];
    var filter_type_id = chartData.filter_id;
    if (filterTypeInput.indexOf(filter_type_id) == -1)
      continue;
    var filterTypeName = getFilterTypeName(filter_type_id);
    compliance_count = [];
    total_count = [];
    compliance_info = chartData.complied_compliance;
    data = [];
    for (var j = 0; j < compliance_info.length; j++) {
      compliance_count.push(compliance_info[j].complied_compliances_count);
      total_count.push(compliance_info[j].total_compliances);
      data.push({
        y: compliance_info[j].complied_compliances_count,
        t: compliance_info[j].total_compliances
      });
    }
    chartDataSeries.push({
      'name': filterTypeName,
      'data': data,
      'total': total_count
    });
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
  applicable = source_data.applicable_count;
  not_applicable = source_data.not_applicable_count;
  not_opted = source_data.not_opted_count;
  total = parseInt(applicable) + parseInt(not_applicable) + parseInt(not_opted);
  if (applicable == 0 && not_applicable == 0 && not_opted == 0) {
  } else {
    if (applicable == 0)
      v_visible = false;
    else
      v_visible = true;
    chartDataSeries.push({
      name: 'Applicable',
      y: applicable,
      drilldown: 'Applicable',
      visible: v_visible
    });
    if (not_applicable == 0)
      v_visible = false;
    else
      v_visible = true;
    chartDataSeries.push({
      name: 'Not Applicable',
      y: not_applicable,
      drilldown: 'Not Applicable',
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
    chartTitle = 'Compliance Applicability Status of ' + GROUP_NAME;
  } else {
    filter_names = [];
    for (var i = 0; i < filterTypeInput.length; i++) {
      name = getFilterTypeName(filterTypeInput[i]);
      filter_names.push(name);
    }
    chartTitle = 'Compliance Applicability Status of ' + chartTitle + ' ' + filter_names;
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
  var requestData = {
    'country_ids': chartInput.getCountries(),
    'domain_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids
  };
  client_mirror.getEscalationChartData(requestData, function (status, data) {
    ESCALATION_DATA = data;
    updateEscalationChart(data);
  });
}
function loadTrendChart() {
  var filter_type = chartInput.getFilterType();
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  var requestData = {
    'country_ids': chartInput.getCountries(),
    'domain_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': [1]
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
  var requestData = {
    'country_ids': chartInput.getCountries(),
    'domain_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids
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
    'country_ids': chartInput.getCountries(),
    'domain_ids': chartInput.getDomains(),
    'filter_type': filterType,
    'filter_ids': filter_ids
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
  if (chartType == 'compliance_status') {
    loadComplianceStatusChart();
  } else if (chartType == 'escalations') {
    loadEscalationChart();
  } else if (chartType == 'not_complied') {
    loadNotCompliedChart();
  } else if (chartType == 'compliance_report') {
    loadAssigneeWiseCompliance();
  } else if (chartType == 'trend_chart') {
    loadTrendChart();
  } else if (chartType == 'applicability_status') {
    loadComplianceApplicabilityChart();
  } else if (chartType == 'assignee_wise_compliance') {
    loadAssignessWiseComplianceChart();
  } else {
    hideLoader();
  }
}