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
          color: '#337ab7',
          textDecoration: 'underline'
        },
        useHTML: true,
        formatter: function () {
          return '<div id="label_' + this.value + '">' + this.value + '</div>';
        }
      },
      tooltip: { pointFormat: '' }
    },
    legend: {
      itemStyle: {
         "fontWeight": "normal",
         "fontSize": "11px",
      }
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
      '#3ec845',
      '#fe6271',
      '#fbca35',
      '#F32D2B'
    ],//      '#A5D17A',  '#F58835',   '#F0F468',   '#F32D2B'

    series: chartDataSeries
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
  $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function (e) {
    var value = this.textContent || this.innerText;
    name = value;
    data_series = drilldownSeries[name];
    var title = chartTitle + ' - ' + name;
    updateComplianceStatusPieChart(data_series, title, 'pie', name);
    complianceDrillDown(data_series, title, name);  // setChart(value);      
    return false;
  });  
}

function updateComplianceStatusPieChart(data_list, chartTitle, chartType, filter_name) {
  $(".graph-selections-bottom").hide();
  hideButtons();
  var total = 0;
  for (var i = 0; i < data_list.length; i++) {
    item = data_list[i];
    total += parseInt(item.y);
  }
  var options = {
    // var options = new Highcharts.Chart({
    colors: [
      '#3ec845',
      '#fe6271',
      '#fbca35',
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
    $("#btn-export").show();
    options.chart.type = 'pie';
    options.chart.options3d = {
      enabled: true,
      alpha: 55,
      beta: 0
    };
    var chart1 = new Highcharts.Chart(options);
    $('.btn-pie-chart').hide();
    $('.btn-bar-chart').show();
  } else {
    $("#btn-export").show();
    options.chart.type = 'column';
    options.legend.enabled = false;
    options.colors = [
      '#3ec845',
      '#fe6271',
      '#fbca35',
      '#F32D2B'
    ];
    var chart1 = new Highcharts.Chart(options);
    $('.btn-pie-chart').show();
    $('.btn-bar-chart').hide();
  }
}
//
// Escalation chart
//
function updateEscalationChart(data) {
  $('.chart-container').show();
  data = prepareEscalationChartdata(data);
  console.log(JSON.stringify(data));
  xAxis = data[0];
  chartDataSeries = data[1];
  chartTitle = data[2];
  highchart = new Highcharts.Chart({
    colors: [
      '#FE6271',
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
      crosshair: true,
      labels: {
        style: {
          cursor: 'pointer',
          color: '#337ab7',
          textDecoration: 'underline'
        },
        useHTML: true,       
      },
    },
    yAxis: {
      min: 0,
      title: { text: 'Total Compliances' },
      allowDecimals: false
    },
    legend: {
      reversed: true,
      itemStyle: {
          fontWeight:'normal',
          fontSize:'11px'
      }
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="padding:0">{series.name}: </td>' +
          '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      series: {
        pointWidth: 40,        
      },
      column: {
        pointPadding: 0,
        groupPadding: 0.26,
        borderWidth: 0,
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
      '#F62025',
      '#FF6052',
      '#F2746B',
      '#FF9C80'
    ],
    chart: {
      renderTo: 'status-container',
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 30
      }
    },
    title: { text: chartTitle },
    xAxis: { categories: true },
    credits: { enabled: false },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f}</b> out of ' + total
    },
    legend: {
      reversed: true,
      itemStyle: {
          fontWeight:'normal',
          fontSize:'11px'
      }
    },
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
      pointFormat: '({point.point.y} out of {point.stackTotal})',
      formatter: function () {
        var s = '<b>' + this.x + '</b>', sum = 0;
        $.each(this.points, function (i, point) {
          total = point.point.t;
          tasks = Math.round(point.point.y * 100 / total, 2);
          color = point.color;
          if(total != "undefined"){
            s += '<br/><span style="color:' + color + '"> <b>' + point.series.name + '</b> </span>: ' + tasks + '% (' + point.point.y + ' out of ' + total + ')';  
          }else{
            s += '<br/><span style="color:' + color + '"> <b>' + point.series.name + '</b> </span>: ' + tasks + '% ()';
          }
          
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
      $("#btn-export").show();
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
      '#FB4739',
      '#F2746B',
      '#DD070C',
      '#FF9C80',
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
  // Possibilities: "group", "business_group", "legal_entity", "division", "category",  "unit", "consolidated"
  this.business_groups = [];
  this.legal_entities = [];
  this.divisions = [];
  this.categories = [];
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
      // return [];
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
      //return [];
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
      // if (this.filter_type == 'business_group') {
        
        ids = get_ids(CHART_FILTERS_DATA.bg_groups, 'bg_id');
        if (this.chart_type == 'compliance_status')
          return ids;
        else
          return [ids[0]];
      // } else
      //   return [];
    }
  };
  this.setLegalEntities = function (v, isAdd, isSingle) {
    v = parseInt(v);
    index = this.legal_entities.indexOf(v);
    if (index >= 0 && !isAdd) {
      this.legal_entities.splice(index, 1);
      return;
    }
    if (isSingle != "multiple") {
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
    // leids = client_mirror.getSelectedLegalEntity();
    // this.legal_entities = $.map(leids, function(element,index) {return element.le_id});
    if (this.legal_entities.length > 0)
      return copyArray(this.legal_entities);
    else {
      //if (this.filter_type == 'legal_entity') {
        ids = get_ids(client_mirror.getSelectedLegalEntity(), 'le_id');
        if (this.chart_type == 'compliance_status')
          return ids;
        else
          return [ids[0]];
      // } else
      //   return [];
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
    if (this.divisions.length > 0){
      console.log(copyArray(this.divisions));
      return copyArray(this.divisions);
    }
    else {
      if (this.filter_type == 'division') {
        ids = get_ids(CHART_FILTERS_DATA.div_infos, 'div_id');
        console.log(ids);
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
// function clearMessage() {
//   $('.chart-error-message').text('');
// }
// function displayMessage(message) {
//   $('.chart-error-message').text(message);
// }
// function hideLoader() {
//   $('.loading-indicator-spin').hide();
// }
// function displayLoader() {
//   $('.loading-indicator-spin').hide();
// }
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
  else if (filter_type == 'category')
    filterIds = chartInput.getCategories();
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
  } else if (chartInput.filter_type == 'category') {
    return chartInput.getCategories();
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
  } else if (chartInput.filter_type == 'category') {
    return CATEGORIES[filter_type_id];
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
  } else if (chartInput.filter_type == 'category') {
    return 'Category';
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
    'category': 'Categories',
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
    var option = getOptionElement(country.c_id, country.c_name, true);

    $('.country-filter').append(option).multiselect('rebuild');
  }
}
function loadDomains() {
  domains = CHART_FILTERS_DATA.d_info;
  for (var i = 0; i < domains.length; i++) {
    var domain = domains[i];
    var option = getOptionElement(domain.d_id, domain.d_name, true);
    $('.domain-filter').append(option).multiselect('rebuild');
  }
}
function loadBusinessGroups(isSelectAll) {
  $(".bg-filter option").remove();
  business_groups = CHART_FILTERS_DATA.bg_groups;
  for (var i = 0; i < business_groups.length; i++) {
    var business_group = business_groups[i];
    var option = getOptionElement(business_group.bg_id, business_group.bg_name, isSelectAll);
    $('.bg-filter').append(option);
  }
  if (business_groups.length == 0) {
    $('.btn-business-group').hide();
  }
}
function loadLegalEntities(isSelectAll) {
  $(".legal-entity-filter option").remove();
  legal_entities = CHART_FILTERS_DATA.le_did_infos;
  for (var i = 0; i < legal_entities.length; i++) {
    var legal_entity = legal_entities[i];
    var option = getOptionElement(legal_entity.le_id, legal_entity.le_name, isSelectAll);
    $('.legal-entity-filter').append(option);
  }
}
function loadDivisions(isSelectAll) {
  $('.division-filter').empty();
  divisions = CHART_FILTERS_DATA.div_infos;
  console.log(JSON.stringify(divisions));
  for (var i = 0; i < divisions.length; i++) {
    var division = divisions[i];
    var option = getOptionElement(division.div_id, division.div_name, isSelectAll);
    $('.division-filter').append(option);
  }
  if (divisions.length == 0) {
    $('.btn-division').hide();
  }
}
function loadCategories(isSelectAll) {
  $('.category-filter').empty();
  categories = CHART_FILTERS_DATA.cat_info;
  for (var i = 0; i < categories.length; i++) {
    var catg = categories[i];
    var option = getOptionElement(catg.cat_id, catg.cat_name, isSelectAll);
    $('.category-filter').append(option);
  }
}
function loadUnits(isSelectAll) {
  $('.unit-filter').empty();
  units = CHART_FILTERS_DATA.assign_units;
  for (var i = 0; i < units.length; i++) {
    var unit = units[i];
    var option = getOptionElement(unit.u_id, unit.u_name, isSelectAll);
    $('.unit-filter').append(option);
  }
}
function loadSubFilters(isSelectAll, isSingleSelect) {
  var selectedLegalentity = client_mirror.getSelectedLegalEntity();
  loadBusinessGroups(isSelectAll);
  loadLegalEntities(isSelectAll);
  loadDivisions(isSelectAll);
  loadCategories(isSelectAll);
  loadUnits(isSelectAll);
  if(selectedLegalentity.length == 1){
    $(".group-selection").hide();
    $(".business-group-selection").hide();
    $(".legal-entity-selection").hide();
  }else{
    // $(".group-selection").show();
    // $(".business-group-selection").show();
    // $(".legal-entity-selection").show();
  }


  business_groups = get_ids(CHART_FILTERS_DATA.bg_groups, 'bg_id');
  chartInput.setBusinessGroupsAll(business_groups);


  legal_entities = get_ids(CHART_FILTERS_DATA.le_did_infos, 'le_id');
  chartInput.setLegalEntitiesAll(legal_entities);


  divisions = get_ids(CHART_FILTERS_DATA.div_infos, 'div_id');
  chartInput.setDivisionsAll(divisions);


  categories = get_ids(CHART_FILTERS_DATA.cat_info, 'cat_id');
  chartInput.setCategoryAll(categories);


  units = get_ids(CHART_FILTERS_DATA.assign_units, 'u_id');
  chartInput.setUnitsAll(units);


  $('.bg-filter').multiselect({
    // filter: true,
    // selectAll: isSelectAll,
    // single: isSingleSelect,
    // placeholder: 'Select Business Group',
    // onDropdownHide: function (business_group) {
    //   chartInput.setBusinessGroups(business_group.value, business_group.checked, isSingleSelect);
    // },
    enableFiltering: true,
    onChange: function(option, checked, select) {
      chartInput.setBusinessGroups(option.val(), checked, isSingleSelect);
    },
    // onSelectAll: function () {
    //   business_groups = get_ids(CHART_FILTERS_DATA.bg_groups, 'bg_id');
    //   chartInput.setBusinessGroupsAll(business_groups);
    // },
    // onDeselectAll: function () {
    //   chartInput.setBusinessGroupsAll([]);
    // }
  });
  if(isSingleSelect == "multiple") {
    $(".bg-filter").attr("multiple", "multiple");
  }else{
    $(".bg-filter").removeAttr("multiple", "multiple");
  }
  $(".bg-filter").multiselect('rebuild');
  $('.legal-entity-filter').multiselect({
    // filter: true,
    // selectAll: isSelectAll,
    // single: isSingleSelect,
    // placeholder: 'Select Legal Entity',
    enableFiltering: true,
    onChange: function(option, checked, select) {
      chartInput.setLegalEntities(option.val(), checked, isSingleSelect);
    },
    // onSelectAll: function () {
    //   legal_entities = get_ids(CHART_FILTERS_DATA.le_did_infos, 'le_id');
    //   chartInput.setLegalEntitiesAll(legal_entities);
    // },
    // onDeselectAll: function () {
    //   chartInput.setLegalEntitiesAll([]);
    // }
  });
  if(isSingleSelect == "multiple"){
    $(".legal-entity-filter").attr("multiple", "multiple");
  }else{
    $(".legal-entity-filter").removeAttr("multiple");
  }
  $(".legal-entity-filter").multiselect('rebuild');

  $('.division-filter').multiselect({
    // filter: true,
    // selectAll: isSelectAll,
    // single: isSingleSelect,
    // placeholder: 'Select Division',
    //   onDropdownHide: function (division) {
    //   chartInput.setDivisions(division.value, division.checked, isSingleSelect);
    // },
     enableFiltering: true,
     onChange: function(option, checked, select) {
      chartInput.setDivisions(option.val(), checked, isSingleSelect);
    },
    // onSelectAll: function () {
    //   divisions = get_ids(CHART_FILTERS_DATA.div_infos, 'div_id');
    //   chartInput.setDivisionsAll(divisions);
    // },
    // onDeselectAll: function () {
    //   chartInput.setDivisionsAll([]);
    // }
  });
  if(isSingleSelect == "multiple"){
    $(".division-filter").attr("multiple", "multiple");
  }else{
    $(".division-filter").removeAttr("multiple");
  }
  $(".division-filter").multiselect('rebuild');
  $('.category-filter').multiselect({
    // filter: true,
    // selectAll: isSelectAll,
    // single: isSingleSelect,
    // placeholder: 'Select Unit',
    //   onDropdownHide: function (catg) {
    //   chartInput.setCategory(catg.value, catg.checked, isSingleSelect);
    // },
    enableFiltering: true,
    onChange: function(option, checked, select) {
      chartInput.setCategory(option.val(), checked, isSingleSelect);
    },
    // onSelectAll: function () {
    //   categories = get_ids(CHART_FILTERS_DATA.cat_info, 'category_id');
    //   chartInput.setCategoryAll(categories);
    // },
    // onDeselectAll: function () {
    //   chartInput.setCategoryAll([]);
    // }
  });
  if(isSingleSelect == "multiple"){
    $('.category-filter').attr("multiple", "multiple");
  }else{
    $('.category-filter').removeAttr("multiple");
  }
  $(".category-filter").multiselect('rebuild');
  $('.unit-filter').multiselect({
    // filter: true,
    // selectAll: isSelectAll,
    // single: isSingleSelect,
    // placeholder: 'Select Unit',
    //   onDropdownHide: function (unit) {
    //   chartInput.setUnits(unit.value, unit.checked, isSingleSelect);
    // },
    enableFiltering: true,
    onChange: function(option, checked, select) {
      chartInput.setUnits(option.val(), checked, isSingleSelect);
    },
    // onSelectAll: function () {
    //   units = get_ids(CHART_FILTERS_DATA.assign_units, 'u_id');
    //   chartInput.setUnitsAll(units);
    // },
    // onDeselectAll: function () {
    //   chartInput.setUnitsAll([]);
    // }
  });
  if(isSingleSelect == "multiple"){
    $('.unit-filter').attr("multiple", "multiple");
  }else{
    $('.unit-filter').removeAttr("multiple");
  }
  $(".unit-filter").multiselect('rebuild');
}
function initializeFilters() {

  loadCountries();

  countries = get_ids(CHART_FILTERS_DATA.countries, 'c_id');
  chartInput.setCountriesAll(countries);

  $('.country-filter').multiselect({
    // buttonWidth: '100%',
    // includeSelectAllOption: true,
    // enableFiltering: true,
    onChange: function (country, checked) {
      chartInput.setCountries(country.val(), checked);
    },
    // onSelectAll: function() {
    //   countries = get_ids(CHART_FILTERS_DATA.countries, 'c_id');
    //   chartInput.setCountriesAll(countries);
    // },
    // onDeselectAll: function () {
    //   chartInput.setCountriesAll([]);
    // }
  });

  loadDomains();
  domains = get_ids(CHART_FILTERS_DATA.d_info, 'd_id');
  chartInput.setDomainsAll(domains);

  $('.domain-filter').multiselect({
    // enableFiltering: true,
    // placeholder: 'Select Domain',
    onChange: function (domain, checked) {
      chartInput.setDomains(domain.val(), checked);
    },
    // onSelectAll: function () {
    //   domains = get_ids(CHART_FILTERS_DATA.d_info, 'd_id');
    //   chartInput.setDomainsAll(domains);
    // },
    // onDeselectAll: function () {
    //   chartInput.setDomainsAll([]);
    // }
  });
  loadSubFilters(selectall = true, singleSelect = "multiple");
  // $('.btn-country').on('click', function () {
  //   $(this).toggleClass('active');
  //   if ($(this).hasClass('active')) {
  //     chartInput.setCountrySelected(true);
  //     $('.country-selection').show();
  //   } else {
  //     chartInput.setCountrySelected(false);
  //     $('.country-selection').hide();
  //   }
  // });
  // $('.btn-domain').on('click', function () {
  //   $(this).toggleClass('active');
  //   if ($(this).hasClass('active')) {
  //     chartInput.setDomainSelected(true);
  //     $('.domain-selection').show();
  //   } else {
  //     chartInput.setDomainSelected(false);
  //     $('.domain-selection').hide();
  //   }
  // });
  // $('.btn-date').on('click', function () {
  //   $(this).toggleClass('active');
  //   if ($(this).hasClass('active')) {
  //     chartInput.setDateSelected(true);
  //     $('.date-selection').show();
  //   } else {
  //     chartInput.setDateSelected(false);
  //     $('.date-selection').hide();
  //   }
  // });
  // $('.btn-date-filter').on('click', function () {
  //   var from_date = $('#fromdate').val();
  //   var to_date = $('#todate').val();
  //   if (from_date.length > 0 && to_date.length > 0) {
  //     chartInput.setFromDate(from_date);
  //     chartInput.setToDate(to_date);
  //     loadCharts();
  //   }
  // });
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
    //$(this).toggleClass('active');
    $(this).prop("checked", true);
    if ($(this).prop("checked", true)) {
      $(".selections").hide();
      $('.chart-filter').prop("checked", false);
      $(this).prop("checked", true);
      $('.' + filter_type_selection).show();
    } else {
      $('.' + filter_type_selection).hide();
    }
    var chart_type = chartInput.getChartType();
    if (filter_type == 'group') {
      loadCharts();
    }
    else if(filter_type == 'consolidated'){
      loadCharts();
      $("#btn-export").hide();
    }
    else{
      $("#btn-export").show();
    }
  });
  $('.btn-go .btn').on('click', function () {
    chartInput.setCountrySelected(true);
    chartInput.setDomainSelected(true);
    var chart_type = chartInput.getChartType();
    loadCharts();
  });
  // $('.btn-go .btn').on('click', function () {
  //   loadCharts();
  // });
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
// function onCountrySuccess(val) {
//   $('#countryval').val(val[1]);
//   $('#country').val(val[0]);
// }
//load country list in autocomplete text box
// function ac_country_load(textval, e) {
//   getCountryAutocomplete(e, textval, COUNTRYLIST, function (val) {
//     onCountrySuccess(val);
//   });
// }
// //retrive legelentity form autocomplete value
// function onLegalEntitySuccess(val) {
//   $('#legalentityval').val(val[1]);
//   $('#legalentityid').val(val[0]);
// }
// //load legalentity form list in autocomplete text box
// function ac_le_load(textval, e) {
//   getClientLegalEntityAutocomplete(e, textval, LEGALENTITYLIST, function (val) {
//     onLegalEntitySuccess(val);
//   });
// }
// //retrive unit form autocomplete value
// function onUnitSuccess(val) {
//   $('#unitval').val(val[1]);
//   $('#unitid').val(val[0]);
// }
// //load unit  form list in autocomplete text box
// function ac_unit_load(textval, e) {
//   //var cId = $("#country").val();
//   //var dId = 0;
//   getUnitAutocomplete(e, textval, UNITLIST, function (val) {
//     onUnitSuccess(val);
//   });
// }
// //retrive businessgroup form autocomplete value
// function onBusinessGroupSuccess(val) {
//   $('#businessgroupsval').val(val[1]);
//   $('#businessgroupid').val(val[0]);
// }
// //load businessgroup form list in autocomplete text box
// function ac_bg_load(textval, e) {
//   getClientBusinessGroupAutocomplete(e, textval, BUSINESSGROUPSLIST, function (val) {
//     onBusinessGroupSuccess(val);
//   });
// }
// //retrive division form autocomplete value
// function onDivisionSuccess(val) {
//   $('#divisionval').val(val[1]);
//   $('#divisionid').val(val[0]);
// }
// //load division form list in autocomplete text box
// function ac_division_load(textval, e) {
//   getClientDivisionAutocomplete(e, textval, DIVISIONLIST, function (val) {
//     onDivisionSuccess(val);
//   });
// }
// //retrive user autocomplete value
// function onUserSuccess(val) {
//   $('#userval').val(val[1]);
//   $('#userid').val(val[0]);
// }
// //load user list in autocomplete text box
// function ac_user_load(textval, e) {
//   getUserAutocomplete(e, textval, USERLIST, function (val) {
//     onUserSuccess(val);
//   });
// }
//
// Prepare chart data
//
function parseComplianceStatusApiInput() {
  var countryIds = chartInput.getCountries();
  var domainIds = chartInput.getDomains();
  if(countryIds == ""){
    displayMessage(message.country_required);
    return false;
  }
  if(domainIds.length == ""){
    displayMessage(message.domain_required);
    return false;
  }
  // TODO: Validation of empty Country / Domain list.
  var filter_type = chartInput.getFilterType();
  var filterIds = getFilterIds(filter_type);
  var filterType = filter_type.replace('_', '-');
  filterType = hyphenatedToUpperCamelCase(filterType);
  var fromDate = $('#fromdate').val();
  var toDate = $('#todate').val();
  if(fromDate == ""){ fromDate = null;}
  if(toDate == ""){ toDate = null;}
  // var fromDate = chartInput.getFromDate();
  // var toDate = chartInput.getToDate();
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
  function sortJSON(data, key, way) {
      return data.sort(function(a, b) {
          var x = a[key]; var y = b[key];
          if (way === '123' ) { return ((x < y) ? -1 : ((x > y) ? 1 : 0)); }
          if (way === '321') { return ((x > y) ? -1 : ((x < y) ? 1 : 0)); }
      });
  }
  chart_data = sortJSON(chart_data,'filter_type_id', '123');  //asc order by filter_type_id

  var temp = {};
  var obj = null;
  for(var i=0; i < chart_data.length; i++) {
     obj=chart_data[i];

     if(!temp[obj.filter_type_id]) {
         temp[obj.filter_type_id] = obj;
     } else {
         //temp[obj.key].val += obj.val;
         temp[obj.filter_type_id].c_data[0]["inprogress_compliance_count"]  += obj.c_data[0]["inprogress_compliance_count"];
         temp[obj.filter_type_id].c_data[0]["not_complied_count"]  += obj.c_data[0]["not_complied_count"];
         temp[obj.filter_type_id].c_data[0]["delayed_compliance_count"]  += obj.c_data[0]["delayed_compliance_count"];
         temp[obj.filter_type_id].c_data[0]["complied_count"]  += obj.c_data[0]["complied_count"];
     }
  }
  var chart_data = [];
  for (var prop in temp)
    chart_data.push(temp[prop]);

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
      // if (parseInt(item.year) != yearInput)
      //   continue;
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

  function sortJSON(data, key, way) {
      return data.sort(function(a, b) {
          var x = a[key]; var y = b[key];
          if (way === '123' ) { return ((x < y) ? -1 : ((x > y) ? 1 : 0)); }
          if (way === '321') { return ((x > y) ? -1 : ((x < y) ? 1 : 0)); }
      });
  }
  chart_data = sortJSON(chart_data,'chart_year', '123');  //asc order by filter_type_id


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

  final_data = {}
  for (var i = 0; i < source_data.trend_data.length; i++) {
    chartData = source_data.trend_data[i];
    // chart_year.push(chartData.chart_year);
    var filter_type_id = chartData.filter_id;
    var filterTypeInput = getFilterTypeInput();
    if (filterTypeInput.indexOf(filter_type_id) == -1)
      continue;
    var filterTypeName = getFilterTypeName(filter_type_id);
    if (final_data[filterTypeName] == undefined) {
      final_data[filterTypeName] = {};
      t_info = {}
      t_info['name'] = filterTypeName;
      t_info['data'] = [{
        'year': chartData.chart_year,
        'y': chartData.complied_compliances_count,
        't': chartData.total_compliances
      }];
      t_info['total'] = chartData.total_compliances;
      final_data[filterTypeName] = t_info;
    }
    else {
      t_info = final_data[filterTypeName];
      year_data = t_info['data'];
      data_added = false;
      $.each(year_data, function(idx, v) {
        if (v['year'] == chartData.chart_year) {
          data_added = true;
          v['y'] += chartData.complied_compliances_count;
          v['t'] += chartData.total_compliances;
        }
      });
      if (data_added == false) {
        year_data.push({
          'year': chartData.chart_year,
          'y': chartData.complied_compliances_count,
          't': chartData.total_compliances
        });
      }
      t_info['data'] = year_data;
      final_data[filterTypeName] = t_info;
    }
  }

  xAxis = [];
  $.each(final_data, function(k, v) {
    chartDataSeries.push(v);

    $.each(v['data'], function(idx, v1) {
      index = xAxis.indexOf(v1['year']);
      if (index == -1) {
        xAxis.push(v1['year']);
      }
    });

  });
  if(xAxis[0] == undefined){
    chartTitle = 'Complied';  
  }else{
    chartTitle = 'Complied (' + xAxis[0] + ' to ' + xAxis[xAxis.length - 1] + ')';  
  } 

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
    if (key == 'T_0_to_30_days_count') {
      chartDataSeries.unshift({
        name: '0-30 days',
        y: item,
        drilldown: 'Below 30',
        visible: v_visible
      });
    } else if (key == 'T_31_to_60_days_count') {
      chartDataSeries.push({
        name: '31-60 days',
        y: item,
        drilldown: 'Below 60',
        visible: v_visible
      });
    } else if (key == 'T_61_to_90_days_count') {
      chartDataSeries.push({
        name: '61-90 days',
        y: item,
        drilldown: 'Below 90',
        visible: v_visible
      });
    } else if (key == 'Above_90_days_count') {
      chartDataSeries.push({
        name: 'Above 90 days',
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
  PageTitle.text("Compliance Status");
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
    $('.btn-group').prop('checked', true);
  });
}
function loadEscalationChart() {
  PageTitle.text("Escalation");
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
  PageTitle.text("Trend Chart");
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
  PageTitle.text("Not Complied");
  var filter_type = chartInput.getFilterType();
  console.log("filter_type--"+filter_type);
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
  PageTitle.text("Risk Report");
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
  PageTitle.text("Assignee Wise Compliances");
  var selectedLegalentity = client_mirror.getSelectedLegalEntity();
  console.log(JSON.stringify(selectedLegalentity));
  if(selectedLegalentity.length == 1){
      CountryVal.val(selectedLegalentity[0]["c_name"]);
      Country.val(selectedLegalentity[0]["c_id"]);
      LegalEntityVal.val(selectedLegalentity[0]["le_name"]);
      LegalEntity.val(selectedLegalentity[0]["le_id"]);
  }
  client_mirror.getAssigneewiseComplianesFilters(function (status, data) {
    updateAssigneeWiseComplianceFiltersList(data);
  });
}
function loadCharts() {
  $("#btn-export").show();
  // displayLoader();
  hideButtons();
  $('.drilldown-container').hide();
  $('.graph-container.compliance-status').show();
  $('.div-drilldown-container').hide();
  $('.chart-container').show();
  $('.graph-selections-bottom').show();
  var chartType = chartInput.getChartType();
  chartInput.setChartYear(0);
  if (chartType == 'compliance_report') {
    $(".filter-button").hide();
    $('.chart-container-inner').hide();
    $('.report-container-inner').show();
    $(".escalation-drilldown-container").hide();
    $(".div-assignee-wise-compliance").show();
    $(".assignee-wise-accordian-list").hide();
    $(".compliance-report-tab-content").show();
    $("#btn-export").hide();

  } else {
    $(".filter-button").show();
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
  $(".assignee-wise").hide();
  $(".div-assignee-wise-compliance").hide();
  $(".assignee-wise").empty();

  // get_ids(CHART_FILTERS_DATA.countries, 'c_id');
  // countries = get_ids(CHART_FILTERS_DATA.countries, 'c_id');
  // chartInput.setCountriesAll(countries);
  
  if (chartType == 'compliance_status') {
    loadComplianceStatusChart();
  } else if (chartType == 'escalations') {
    loadEscalationChart();
  } else if (chartType == 'not_complied') {
    loadNotCompliedChart();
  } else if (chartType == 'compliance_report') {
    $(".drilldown-container").empty();
    $(".div-assignee-wise-compliance").hide();
    loadAssigneeWiseCompliance();
  } else if (chartType == 'trend_chart') {
    loadTrendChart();
  } else if (chartType == 'applicability_status') {
    loadComplianceApplicabilityChart();
  }
  // else if (chartType == 'assignee_wise_compliance') {
  //   PageTitle.html("Assignee Wise Compliances");
  //   loadAssigneeWiseComplianceChart();
  // }
  else {
    hideLoader();
  }
}
function Compliance_Status_Export() {
    cols = ["Country", "Complied", "Delayed Compliance", "Inprogress", "Not Complied"];
    if (chartInput.getFilterType() != "group") {
      c = getFilterTypeTitle();
      if (c == null) {
        cols[0] = "Nil";
      }
      else {
        cols[0] = c;
      }
    }
    final_dict = {}
    $.each(COMPLIANCE_STATUS_DATA, function(k,v) {
      c_data = v.c_data;
      var d = {}
      if (final_dict[v.filter_type_id] == undefined) {
        d[cols[0]] = getFilterTypeName(v.filter_type_id);
        d[cols[1]] = 0;
        d[cols[2]] = 0;
        d[cols[3]] = 0;
        d[cols[4]] = 0;
      }
      else {
        d = final_dict[v.filter_type_id];
      }

      $.each(c_data, function(kk, vv) {
        d[cols[1]] += vv.complied_count;
        d[cols[2]] += vv.delayed_compliance_count;
        d[cols[3]] += vv.inprogress_compliance_count;;
        d[cols[4]] += vv.not_complied_count;;
      });
      final_dict[v.filter_type_id] = d;
    });
    data = []
    data.push({"col1": "Compliance Status Graph"});
    keys = Object.keys(final_dict);
    labels = {}
    labels['col1'] = cols[0];
    labels['col2'] = cols[1];
    labels['col3'] = cols[2];
    labels['col4'] = cols[3];
    labels['col5'] = cols[4];
    data.push(labels);

    $.each(final_dict, function(k, v) {
      info = {}
      keys = Object.keys(v);
      $.each(keys, function(idx, val) {
        info['col' + idx] = v[val];
      });
      data.push(info);
    });
    client_mirror.exportJsontoCsv(data, "Compliance Status Graph");
}
function Escalation_Export() {
  cols = ["Years"];
  final_dict = {};

  $.each(ESCALATION_DATA.es_chart_data, function(k, v) {
    if (final_dict[v.chart_year] == undefined) {
      d = {};
      d["not_complied_count"] = v.not_complied_count;
      d["delayed_compliance_count"] = v.delayed_compliance_count;
      final_dict[v.chart_year] = d ;
    }
    else {
      d = final_dict[v.chart_year];
      d["not_complied_count"] += v.not_complied_count;
      d["delayed_compliance_count"] += v.delayed_compliance_count;
      final_dict[v.chart_year] = d ;
    }
  });
  data = [];
  $.merge(cols, Object.keys(final_dict));
  data.push({"col0": "Escalation Graph"});
  years = {};
  delays = {};
  nots = {};
  var i = 1;
  years['col0'] = "Year";
  delays['col0'] = "Delayed";
  nots['col0'] = "Not Complied";
  $.each(final_dict, function(k, v) {
    if (v.delayed_compliance_count == 0 && v.not_complied_count == 0){
      return;
    }
    years['col' + i] = k;
    delays['col' + i] = v.delayed_compliance_count;
    nots['col' + i] = v.not_complied_count;
    i += 1;
  });
  data.push(years);
  data.push(delays);
  data.push(nots);
  client_mirror.exportJsontoCsv(data, "Escalation Status Graph");
}

function Notcomplied_Export() {
  cols = ["Ageing", "Count", "Percentage"];
  var vals = Object.keys(NOT_COMPLIED_DATA).map(k => NOT_COMPLIED_DATA[k]);
  var total = vals.reduce(function(a, b) { return a + b; }, 0);
  data = [];
  Below30 = NOT_COMPLIED_DATA.T_0_to_30_days_count;
  Below60 = NOT_COMPLIED_DATA.T_31_to_60_days_count;
  Below90 = NOT_COMPLIED_DATA.T_61_to_90_days_count;
  Above90 = NOT_COMPLIED_DATA.Above_90_days_count;
  data.push({'col0': "Not Complied Graph"});
  data.push({'col0': cols[0], 'col1': cols[1], 'col2': cols[2]});
  data.push({
    "col0" : "0 - 30 days",
    "col1" : Below30,
    "col2" : Math.round((Below30/total) * 100) + '%',
  });
  data.push({
    "col0" : "31 - 60 days",
    "col1" : Below60,
    "col2" : Math.round((Below60/total) * 100) + '%',
  });
  data.push({
    "col0" : "61 - 90 days",
    "col1" : Below90,
    "col2" : Math.round((Below90/total) * 100) + '%',
  });
  data.push({
    "col0" : "Above days",
    "col1" : Above90,
    "col2" : Math.round((Above90/total) * 100) + '%',
  });
  client_mirror.exportJsontoCsv(data, "Not Complied Graph");
}
function TrendChart_Export() {
  final_dict = {};
  temp_count = {};
  cols = [];
  $.each(TREND_CHART_DATA.trend_data, function(k,v) {
    var fname = getFilterTypeName(v.filter_id);
    var total = v.total_compliances;
    var complied = v.complied_compliances_count ;
    var year = parseInt(v.chart_year);

    if (final_dict[fname] == undefined) {
      d = {};
      cols.push(year);
      d[year] = Math.round((complied/total) * 100);
      final_dict[fname] = d;
      c = {};
      c[year] = 1;
      temp_count[fname] = c;
    }
    else {
      if (final_dict[fname][year] == undefined) {

        cols.push(year);

        final_dict[fname][year] = Math.round((complied/total) * 100);;

        temp_count[fname][year] = 1;
      }
      else {
        cnt = final_dict[fname][year];
        cnt += Math.floor((complied/total) * 100);
        final_dict[fname][year] = cnt;
        temp_count[fname][year] += 1;
      }
    }
  });
  data = [];
  data.push({"col0": "Trend Chart"});
  labels = {}
  labels['col0'] = "Country";
  cols.sort(function(a, b){return a-b});
  for (var i = 0; i < cols.length; i++) {
    labels['col'+i+1] = cols[i];
  }
  data.push(labels);

  $.each(final_dict, function(k, v) {      
      info = {}
      info['col0'] = k ;
      for (var i=0; i<cols.length; i++) {        
        if (v[cols[i]] == undefined) {
          yearvals = 0;
        }
        else {
          yearvals = (parseInt(v[cols[i]]) / temp_count[k][cols[i]]);
        }

        info['col'+i+1] = yearvals + '%';
      }
    data.push(info);
  });
  client_mirror.exportJsontoCsv(data, "Trend Chart");
}

function RiskChart_Export() {
  reject = COMPLIANCE_APPLICABILITY_DATA.rejected_count;
  notcomplied = COMPLIANCE_APPLICABILITY_DATA.not_complied_count;
  unassign = COMPLIANCE_APPLICABILITY_DATA.unassign_count;
  notopted = COMPLIANCE_APPLICABILITY_DATA.not_opted_count;
  total = reject + notcomplied + unassign + notopted;
  reject = Math.round((reject/total) * 100) + '%';
  notcomplied = Math.round((notcomplied/total) * 100) + '%';
  unassign = Math.round((unassign/total) * 100) + '%';
  notopted = Math.round((notopted/total) * 100) + '%';
  data = [];
  data.push({"col0": "Risk Graph"});
  data.push({"col0": "Not Complied", "col1": "Rejected", "col2": "Not Opted", "col3": "Un assigned"});
  data.push({"col0": notcomplied, "col1": reject, "col2": notopted, "col3": unassign});
  client_mirror.exportJsontoCsv(data, "Risk Graph");
}

$('#btn-export').on('click', function(){
  // Possiblities: "compliance_status", "escalations", "not_complied", "compliance_report", "trend_chart", "applicability_status"
  if (chartInput.chart_type == "compliance_status") {
      Compliance_Status_Export();
  }
  else if (chartInput.chart_type == "escalations") {
      Escalation_Export();
  }
  else if (chartInput.chart_type == "not_complied") {
      Notcomplied_Export();
  }
  else if (chartInput.chart_type == "trend_chart") {
      TrendChart_Export();
  }
  else if (chartInput.chart_type == "applicability_status") {
      RiskChart_Export();
  }
  // client_mirror.downloadTaskFile();

});

