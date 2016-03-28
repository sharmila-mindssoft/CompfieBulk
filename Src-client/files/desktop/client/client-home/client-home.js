var CHART_FILTERS_DATA = null;
var COUNTRIES = {};
var DOMAINS = {};
var BUSINESS_GROUPS = {};
var LEGAL_ENTITIES = {};
var DIVISIONS = {};
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
var USERLIST = null;
var UNITLIST = null;
var DOMAINLIST = null;

function clearMessage() {
    $(".chart-error-message").text("");
}

function displayMessage(message) {
    $(".chart-error-message").text(message);
}

function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function displayLoader() {
    $(".loading-indicator-spin").hide();
}

function getOptionElement (v, t, selected) {
    var option = $("<option></option>");
    option.val(v);
    option.text(t);
    if (selected) {
        option.attr("selected", true);
    }
    return option;
}

function get_ids (source, key) {
    var ids = [];
    for (var i = 0; i < source.length; i++) {
        var item = source[i];
        ids.push(item[key]);
    };
    return ids;
}

function copyArray(array) {
    return array.slice(0);
}

function ChartInput () {
    this.chart_type = "compliance_status"; // Possiblities: "compliance_status", "escalations", "not_complied", "compliance_report", "trend_chart", "applicability_status"
    this.country_selected = false;
    this.countries = [];
    this.domain_selected = false;
    this.domains = [];
    this.date_selected = false;
    this.from_date = "";
    this.to_date = "";
    this.filter_type = "group"; // Possibilities: "group", "business_group", "legal_entity", "division", "unit", "consolidated"
    this.business_groups = [];
    this.legal_entities = [];
    this.divisions = [];
    this.units = [];
    this.chart_year = 0; // previous_year = 1, current_year = 0, next_year = -1
    this.current_year = (new Date()).getFullYear();
    this.range_index = 7;


    this.setChartType = function (v) {
        this.chart_type = v;
    }

    this.getChartType = function () {
        return this.chart_type;
    }

    this.setCountrySelected = function (v) {
        this.country_selected = v;
    }

    this.setCountries = function (country_id, isAdd) {
        country_id = parseInt(country_id);
        index = this.countries.indexOf(country_id)
        if (index >= 0 && !isAdd) {
            this.countries.splice(index, 1);
            return;
        }
        if (isAdd) {
            this.countries.push(country_id);
        }
    }

    this.setCountriesAll = function (countries) {
        this.countries = copyArray(countries);
    }

    this.getCountries = function () {
        if (this.country_selected) {
            if (this.countries.length > 0)
                return copyArray(this.countries);
            else
                return [];
        }
        else {
            get_ids(CHART_FILTERS_DATA.countries, "country_id");
            countries = get_ids(CHART_FILTERS_DATA.countries, "country_id");
            chartInput.setCountriesAll(countries);
            return countries
        }
    }

    this.setDomainSelected = function (v) {
        this.domain_selected = v;
    }

    this.setDomains = function (domain_id, isAdd) {
        domain_id = parseInt(domain_id);
        index = this.domains.indexOf(domain_id)
        if (index >= 0 && !isAdd) {
            this.domains.splice(index, 1);
            return;
        }
        if (isAdd) {
            this.domains.push(domain_id);
        }
    }

    this.setDomainsAll = function (domains) {
        this.domains = copyArray(domains);
    }

    this.getDomains = function () {
        if (this.domain_selected) {
            if (this.domains.length > 0)
                return copyArray(this.domains);
            else
                return [];
        }
        else{
            domains = get_ids(CHART_FILTERS_DATA.domains, "domain_id");
            chartInput.setDomainsAll(domains);
            return domains;
        }

    }

    this.setDateSelected = function (v) {
        this.date_selected = v;
    }

    this.setFromDate = function (v) {
        this.from_date = v;
    }

    this.getFromDate = function () {
        if (this.date_selected)
            return this.from_date;
        else
            return null;
    }

    this.setToDate = function (v) {
        this.to_date = v;
    }

    this.getToDate = function () {
        if (this.date_selected)
            return this.to_date;
        else
            return null;
    }

    this.setFilterType = function (v) {
        this.filter_type = v;
    }

    this.getFilterType = function () {
        return this.filter_type;
    }

    this.setBusinessGroups = function (v, isAdd) {
        v = parseInt(v);
        index = this.business_groups.indexOf(v)
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
    }

    this.setBusinessGroupsAll = function (business_groups) {
        this.business_groups = copyArray(business_groups);
    }

    this.getBusinessGroups = function () {
        if (this.business_groups.length > 0)
            return copyArray(this.business_groups);
        else {
            if (this.filter_type == "business_group")
                return get_ids(
                    CHART_FILTERS_DATA.business_groups, "business_group_id"
                );
            else
                return [];
        }
    }

    this.setLegalEntities = function (v, isAdd) {
        v = parseInt(v);
        index = this.legal_entities.indexOf(v)
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
    }

    this.setLegalEntitiesAll = function (legal_entities) {
        this.legal_entities = copyArray(legal_entities);
    }

    this.getLegalEntities = function () {
        if (this.legal_entities.length > 0)
            return copyArray(this.legal_entities);
        else {
            if (this.filter_type == "legal_entity")
                return get_ids(
                    CHART_FILTERS_DATA.legal_entities, "legal_entity_id"
                );
            else
                return [];
        }
    }

    this.setDivisions = function (v, isAdd) {
        v = parseInt(v);
        index = this.divisions.indexOf(v)
        if (index >= 0 && !isAdd) {
            this.divisions.splice(index, 1);
            return;
        }
        if (isSingle) {
            this.divisions = [v];
        }
        else {
            if (isAdd) {
                this.divisions.push(v);
            }
        }
    }

    this.setDivisionsAll = function (divisions) {
        this.divisions = copyArray(divisions);
    }

    this.getDivisions = function () {
        if (this.divisions.length > 0)
            return copyArray(this.divisions);
        else {
            if (this.filter_type == "division")
                return get_ids(
                    CHART_FILTERS_DATA.divisions, "division_id"
                );
            else
                return [];
        }
    }

    this.setUnits = function (v, isAdd, isSingle) {
        v = parseInt(v);
        index = this.units.indexOf(v)
        if (index >= 0 && !isAdd) {
            this.units.splice(index, 1);
            return;
        }
        if (isSingle) {
            this.units = [v];
        }
        else {
            if (isAdd) {
                this.units.push(v);
            }
        }
    }

    this.setUnitsAll = function (units) {
        this.units = copyArray(units);
    }

    this.getUnits = function () {
        if (this.units.length > 0)
            return copyArray(this.units);
        else {
            if (this.filter_type == "unit"){
                ids = get_ids(
                    CHART_FILTERS_DATA.units, "unit_id"
                );
                //console.log(ids)
                return ids;
            }
            else
                return [];
        }
    }

    this.setChartYear = function (v) {
        this.chart_year = v;
    }

    this.getChartYear = function () {
        return this.chart_year;
    }

    this.setCurrentYear = function(v) {
        this.current_year = v;
    }

    this.getCurrentYear = function() {
        return this.current_year;
    }

    this.setRangeIndex = function(v) {
        this.range_index += v;
    }
    this.getRangeIndex = function () {
        return this.range_index;
    }
}

var chartInput = new ChartInput();


//
// loadCharts
//

function getFilterIds (filter_type) {
    var filterIds = null;
    if (filter_type.trim() == "business_group"){
        filterIds = chartInput.getBusinessGroups();
    }
    else if (filter_type == "legal_entity")
        filterIds = chartInput.getLegalEntities();
    else if (filter_type == "division")
        filterIds = chartInput.getDivisions();
    else if (filter_type == "unit")
        filterIds = chartInput.getUnits();
    return filterIds;
}

function parseComplianceStatusApiInput () {
    var countryIds = chartInput.getCountries();
    var domainIds = chartInput.getDomains();
    // TODO: Validation of empty Country / Domain list.
    var filter_type = chartInput.getFilterType();
    var filterIds = getFilterIds(filter_type);
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    var fromDate = chartInput.getFromDate();
    var toDate = chartInput.getToDate();
    var chart_year = chartInput.getChartYear();
    if (chart_year == 0) {
        chart_year = chartInput.getCurrentYear();
    }
    var requestData = {
        "country_ids": countryIds,
        "domain_ids": domainIds,
        "filter_type": filterType,
        "filter_ids": filterIds,
        "from_date": fromDate,
        "to_date": toDate,
        "chart_year": chart_year
    };
    return requestData;
}

function getFilterTypeInput () {
    if ((chartInput.filter_type == "group") || (chartInput.filter_type == "consolidated")) {
        return chartInput.getCountries();
    }
    else if (chartInput.filter_type == "business_group") {
        return chartInput.getBusinessGroups();
    }
    else if (chartInput.filter_type == "legal_entity") {
        return chartInput.getLegalEntities();
    }
    else if (chartInput.filter_type == "division") {
        return chartInput.getDivisions();
    }
    else if (chartInput.filter_type == "unit") {
        return chartInput.getUnits();
    }
    else {
        return null;
    }
}

function getFilterTypeName (filter_type_id) {
    if (chartInput.filter_type == "group") {
        return COUNTRIES[filter_type_id];
    }
    else if (chartInput.filter_type == "business_group") {
        return BUSINESS_GROUPS[filter_type_id];
    }
    else if (chartInput.filter_type == "legal_entity") {
        return LEGAL_ENTITIES[filter_type_id];
    }
    else if (chartInput.filter_type == "division") {
        return DIVISIONS[filter_type_id];
    }
    else if (chartInput.filter_type == "unit") {
        return UNITS[filter_type_id];
    }
    else {
        return null;
    }
}

function getFilterTypeTitle () {
    if (chartInput.filter_type == "group") {
        return "Country";
    }
    else if (chartInput.filter_type == "business_group") {
        return "Business Group";
    }
    else if (chartInput.filter_type == "legal_entity") {
        return "Legal Entity";
    }
    else if (chartInput.filter_type == "division") {
        return "Division";
    }
    else if (chartInput.filter_type == "unit") {
        return "Unit";
    }
    else if (chartInput.filter_type == "consolidated"){
        return "Consolidated";
    }
    else {
        return null;
    }
}

function getXAxisName () {
    xAxisNames = {
        "group": "Countries",
        "business_group": "Business Groups",
        "legal_entity": "Legal Entities",
        "division": "Divisions",
        "unit": "Units"
    }
    var filterType = chartInput.getFilterType();
    return xAxisNames[filterType];
}

function hideButtons() {
    $(".btn-back").hide();
    $(".btn-pie-chart").hide();
    $(".btn-bar-chart").hide();
}
function showPreviousNext() {
    $(".btn-previous").show();
    $(".btn-next").show();
}
function hidePreviousNext() {
    $(".btn-previous").hide();
    $(".btn-next").hide();
}


//  Compliance Status Chart

function prepareComplianceStatusChartData (chart_data) {
    // var currentYear = (new Date()).getFullYear();
    var yearInput = chartInput.getCurrentYear()
    // var yearInput = currentYear - chartInput.getChartYear();
    // console.log(yearInput)
    var chartTitle = getFilterTypeTitle()
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
        var filter_type_id = chartData["filter_type_id"];
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
        for (var j = 0; j < chartData["data"].length; j++) {
            var item = chartData["data"][j];
            if (parseInt(item["year"]) != yearInput)
                continue;

            compliedCount += item["complied_count"];
            delayedCount += item["delayed_compliance_count"];
            inprogressCount += item["inprogress_compliance_count"];
            notCompliedCount += item["not_complied_count"];
        };

        if (
            (compliedCount == 0) &&
            (delayedCount == 0) &&
            (inprogressCount == 0) &&
            (notCompliedCount == 0)
        ) {
            continue;
        }
        xAxis.push(filterTypeName);
        xAxisIds.push(filter_type_id);
        yAxisComplied.push(compliedCount);
        yAxisDelayed.push(delayedCount);
        yAxisInprogress.push(inprogressCount);
        yAxisNotComplied.push(notCompliedCount);

    };
    // if (xAxis.length == 0)
    //     return null;
    var xAxisName = getXAxisName();
    var yAxis = ["Complied", "Delayed Compliance", "Inprogress", "Not Complied"];
    var yAxisData = [
        yAxisComplied, yAxisDelayed, yAxisInprogress, yAxisNotComplied
    ];
    function sum_values(arr) {
        var sum = arr.reduce(function(pv, cv) { return pv + cv; }, 0);
        return sum
    }
    if (chartTitle == "Consolidated") {
        data_series = [];
        for (var i=0; i < yAxis.length; i++) {
            data_series.push({
                "name": yAxis[i],
                "y": sum_values(yAxisData[i]),
            });
        }
        return data_series;
    }
    var chartDataSeries = [];
    for (var i = 0; i < yAxis.length; i++) {
        values = yAxisData[i]
        y_list = [];
        for (var x=0; x< values.length; x++) {
            y_list.push({
                "y": values[x],
                "drilldown": yAxis[i],
                "filter_type_id": xAxisIds[x]
            });
        }
        chartDataSeries.push({
            "name": yAxis[i],
            "data": y_list
        });
    };
    var xAxisDrillDownSeries = {};
    for (var j = 0; j < xAxis.length; j++) {
        data_list = []
        for (var x1 = 0; x1 < yAxis.length; x1++) {
            value = yAxisData[x1][j]
            data_list.push({
                "name": yAxis[x1],
                "y": value,
                "filter_id": xAxisIds[j],
                "drilldown": xAxis[j]
            });
        }
        xAxisDrillDownSeries[xAxis[j]] = data_list
    }
    chartTitle =  chartTitle + " wise compliances";
    //console.log(chartDataSeries)
    return [xAxisName, xAxis, chartDataSeries, chartTitle, xAxisDrillDownSeries];
}

function updateComplianceStatusChart (data) {
    var data = prepareComplianceStatusChartData(data);
    if (data == null)
        return;
    chartType = getFilterTypeTitle();
    if (chartType == "Consolidated") {
        chartTitle = "Consolidated Chart";
        updateComplianceStatusPieChart(data, chartTitle, "pie", null)
        hideButtons()
    }
    else {
        $(".graph-container").hide();
        $(".drilldown-container").hide();
        $(".graph-container.compliance-status").show();
        $(".graph-selections-bottom").show();
        currentYear = chartInput.getCurrentYear();
        chartYear = chartInput.getChartYear();
        range = chartInput.getRangeIndex();
        if (chartYear == 0 || chartYear == currentYear){
            $(".btn-next-year").hide();
        }
        else {
            $(".btn-next-year").show();
        }
        if ((currentYear - 7) == chartYear) {
            $(".btn-previous-year").hide();
        }
        else {
            $(".btn-previous-year").show();
        }
        $(".btn-back").on("click", function() {
            updateComplianceStatusStackBarChart(data);
            hideButtons()
        });
        updateComplianceStatusStackBarChart(data);
    }
}

function updateComplianceStatusStackBarChart(data) {
    var xAxisName = data[0];
    var xAxis = data[1];
    var chartDataSeries = data[2];
    var chartTitle = data[3];
    var drilldownSeries = data[4]
    var yAxisname = ["Complied", "Delayed Compliance", "Inprogress", "Not Complied"];

    var highchart;
    // function setChart(name) {
    //     data_series = drilldownSeries[name];
    //     var title = chartTitle + " - " + name;
    //     updateComplianceStatusPieChart(data_series, title, "pie");
    //     complianceDrillDown(data_series, title);
    // }
    // $(".graph-container.compliance-status").highcharts({
    highchart = new Highcharts.Chart({
        chart: {
            renderTo: "status-container",
            type: 'bar',
            width: '850'
        },
        title: {
            text: chartTitle
        },
        credits: {
            enabled: false
        },
        xAxis: {

            categories: xAxis,
            title: {
                text: xAxisName,
            },
            labels: {
                style: {
                    cursor: 'pointer',
                    color: "blue",
                    textDecoration: "underline",
                },
                useHTML: true,
                formatter: function() {
                    return '<div id="label_'+this.value +'">'+this.value+'</div>';
                }
            },
            tooltip: {
                pointFormat: 'sfosdfksdfjds'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total compliances'
            },
            allowDecimals: false,
            reversedStacks: false
        },
        tooltip: {
            headerFormat: '<b>{point.series.name}</b>: {point.percentage:.0f}% ',
            pointFormat: '({point.y} out of {point.stackTotal})'
        },
        plotOptions: {
            series: {
                pointWidth: 35
            },
            bar: {
                stacking: "normal",
                cursor: "pointer",
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
                        click: function() {
                            var drilldown = this.drilldown;
                            if (drilldown) {
                                filter_name = xAxis[this.x];
                                loadComplianceStatusDrillDown(drilldown, this.filter_type_id, filter_name);
                            }
                        }
                    }
                }
            },
        },
        colors: ['#A5D17A', '#F58835', '#F0F468', '#F32D2B'],
        series: chartDataSeries,
    });
    $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
        var value = (this.textContent || this.innerText);
        name = value;
        data_series = drilldownSeries[name];
        var title = chartTitle + " - " + name;
        updateComplianceStatusPieChart(data_series, title, "pie", name);
        complianceDrillDown(data_series, title, name);
        // setChart(value);
    });
    year = chartInput.getChartYear();
    if (year == 0) {
        year = chartInput.getCurrentYear();
    }
    domain_ids = chartInput.getDomains();
    domain_names = [];
    for (var x=0; x < domain_ids.length; x++) {
        id = domain_ids[x];
        domain_names.push(DOMAINS[id]);
    }
    $.each(DOMAIN_INFO, function(key, value) {
        frame_title = "Year : " + year + "\n"
        for (var i = 0; i< value.length; i++) {
            info = value[i]
            if (domain_names.indexOf(info["domain_name"]) != -1){
                frame_title += "" + info["domain_name"] + " : " + info["period_from"] + " to " + info["period_to"] + "\n"
            }
        }
        $("#label_" + key).attr({placement: 'bottom', title: frame_title});
    });
    // $("#label_India").attr({placement: 'bottom', title:"HELLO India!"});
}

function complianceDrillDown(data_list, chartTitle, filter_name) {
    $(".btn-bar-chart").on("click", function () {
        updateComplianceStatusPieChart(data_list, chartTitle, "column", filter_name);
    });
    $(".btn-pie-chart").on("click", function () {
        updateComplianceStatusPieChart(data_list, chartTitle, "pie", filter_name);
    });
}

function updateComplianceStatusPieChart(data_list, chartTitle, chartType, filter_name) {
    var total = 0;
    for (var i=0; i < data_list.length; i++) {
        item = data_list[i];
        total += parseInt(item["y"]);
    }
    var options = {
    // var options = new Highcharts.Chart({
        colors:['#A5D17A','#F58835', '#F0F468', '#F32D2B'],
        chart: {
            renderTo: "status-container",
            width: '850'
        },
        title: {
            text: chartTitle
        },
        xAxis: {
            categories: true,
            title: {
                text: 'Compliance Status'
            }
        },
        yAxis: {
            title: {
                text: 'Total compliances'
            }
        },
        tooltip: {
              headerFormat : '',
            pointFormat: '{point.name}:{point.y} Out of ' + total

        },
        legend: {
            enabled: true
        },
        plotOptions: {
            series: {
                pointWidth: 50
            },
            column: {
                colorByPoint: true,
                point: {
                    events: {
                        click: function() {
                            var drilldown = this.drilldown;
                            if (drilldown) {
                              loadComplianceStatusDrillDown(this.name, this.filter_id, filter_name)
                            }
                        }
                    }
                }
            },
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 45,
                dataLabels: {
                    enabled: true,
                    format: '{point.percentage:.0f}%'
                },
                showInLegend: true,
                point: {
                    events: {
                        click: function() {
                            var drilldown = this.drilldown;
                            if (drilldown) {
                              loadComplianceStatusDrillDown(this.name, this.filter_id, filter_name)
                            }
                        }
                    }
                }
            }
        },
        series: [{
            data: data_list
        }]
    };
    $(".btn-back").show();
    if (chartType == "pie") {
        $(".btn-pie-chart").hide();
        $(".btn-bar-chart").show();
        options.chart.type = 'pie';
        options.chart.options3d = {
            enabled: true,
            alpha: 35,
            beta: 0
        };
        var chart1 = new Highcharts.Chart(options);

    } else {
        $(".btn-pie-chart").show();
        $(".btn-bar-chart").hide();
        options.chart.type = 'column';
        options.legend.enabled = false;
        options.colors = ['#A5D17A','#F58835', '#F0F468', '#F32D2B'];
        var chart1 = new Highcharts.Chart(options);
    }
}

function updateCharts () {
    var chartType = chartInput.getChartType();
    if (chartType == "compliance_status") {
        updateComplianceStatusChart(COMPLIANCE_STATUS_DATA);
        hideLoader();
    }
}

function updateDrillDown(status, data, filterTypeName) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showDrillDownRecord(status, data, filterTypeName);
}

function updateEscalationDrillDown(data, year) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showEscalationDrillDownRecord(data, year);
}

function updateNotCompliedDrillDown(status, data) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showNotCompliedDrillDownRecord(data);
}

function updateComplianceApplicabilityDrillDown(status, data, type) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showComplianceApplicabilityDrillDownRecord(data, type);
}

function showComplianceApplicabilityDrillDownRecord(data, type){
    $(".drilldown-title").text(GROUP_NAME+" - "+type+" Compliances");

    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();
    $(".escalation-drilldown-list .td-escalation").empty();
    var data =  data['drill_down_data'];
    var sno = 1;
    var count = 1;
    var tableHeading = $('#templates .compliance-applicable-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);
    $.each(data, function(key, value){
        var tableUnit = $('#templates .compliance-applicable-status .tr-unit');
        var cloneUnit = tableUnit.clone();
        $(".unit-heading", cloneUnit).html(value["level1_statutory_name"]);
        $(".table-drilldown-list").append(cloneUnit);
        $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
        if(count==1){
            $('.accordion-content'+count).addClass("default");
        }
        var unitList = value["compliances"];
        $.each(unitList, function(ke, valu){
            var tableLevel1 = $('#templates .compliance-applicable-status .tr-level1');
            var cloneLevel1 = tableLevel1.clone();
            var disp_unitname = '';
            for(unit in units){
                if(units[unit]["unit_id"] == ke){
                    disp_unitname = units[unit]["unit_name"]
                }
            }
            $(".heading", cloneLevel1).html(disp_unitname);
            $('.accordion-content'+count).append(cloneLevel1);
            $.each(valu, function(k, val){
                var frequency =  val["frequency"];
                var statutory_date =  val["statutory_dates"];
                var statutorydate = '';
                var triggerbefore = '';
                var summary = val["summary"];

                for(j = 0; j < statutory_date.length; j++){
                  var sDay = '';
                  if(statutory_date[j]["statutory_date"] != null) sDay = statutory_date[j]["statutory_date"];

                  var sMonth = '';
                  if(statutory_date[j]["statutory_month"] != null) sMonth = statutory_date[j]["statutory_month"];

                  var tBefore = '';
                  if(statutory_date[j]["trigger_before_days"] != null) tBefore = statutory_date[j]["trigger_before_days"] + " Days";

                  if(sMonth == 1) sMonth = "Jan"
                  else if(sMonth == 2) sMonth = "Feb"
                  else if(sMonth == 3) sMonth = "Mar"
                  else if(sMonth == 4) sMonth = "Apr"
                  else if(sMonth == 5) sMonth = "May"
                  else if(sMonth == 6) sMonth = "Jun"
                  else if(sMonth == 7) sMonth = "Jul"
                  else if(sMonth == 8) sMonth = "Aug"
                  else if(sMonth == 9) sMonth = "Sep"
                  else if(sMonth == 10) sMonth = "Oct"
                  else if(sMonth == 11) sMonth = "Nov"
                  else if(sMonth == 12) sMonth = "Dec"

                  statutorydate +=  sDay +' - '+ sMonth + ', ';
                  triggerbefore +=  tBefore + ', ';
                }

                if(summary != null){
                  if(statutorydate.trim() != ''){
                    statutorydate = statutorydate.replace(/,\s*$/, "");
                    statutorydate = summary + ' ('+statutorydate+')';
                  }else{
                    statutorydate = summary;
                  }
                }

                if(triggerbefore != ''){
                    triggerbefore = triggerbefore.replace(/,\s*$/, "");
                }
                var tableRow = $('#templates .compliance-applicable-status .table-row-list');
                var clone = tableRow.clone();

                var cDescription = val["description"];
                var partDescription = cDescription;
                if (cDescription != null && cDescription.length > 50){
                  partDescription = cDescription.substring(0,49)+'...';
                }

                var cPenalConsequences = val["penal_consequences"];
                var partPenalConsequences = cPenalConsequences;
                if (cPenalConsequences != null && cPenalConsequences.length > 50){
                  partPenalConsequences = cPenalConsequences.substring(0,49)+'...';
                }

                $(".sno", clone).html(sno);
                $(".statutory-name", clone).html(val["statutory_provision"]);
                var download_url = val["download_url"];
                if(download_url == null){
                    $(".compliance-task-name", clone).html(val["compliance_task"])
                }else{
                    $('.compliance-task-name', clone).html('<a href= "'+ download_url +'" target="_new">'+val["compliance_task"]+'</a>');
                }

                $(".compliance-description-name", clone).html('<abbr class="page-load" title="'+
          cDescription+'">'+partDescription+'</abbr>');
                $(".penal-consequences-name", clone).html('<abbr class="page-load" title="'+
          cPenalConsequences+'">'+partPenalConsequences+'</abbr>');
                $(".compliance-frequency-name", clone).html(frequency);
                $(".repeats", clone).html(statutorydate);
                //$(".statutory-date", clone).html(statutorydate);
                $(".trigger-before", clone).html(triggerbefore);
                $('.accordion-content'+count).append(clone);
                sno = sno + 1;
            });
        });
        count = count + 1;
    });
    accordianType('accordion', 'accordion-toggle', 'accordion-content');
}

function accordianType(idtype, toggleClass, contentClass){
    $('#'+idtype).find('.'+toggleClass).click(function(){
        $(this).next().slideToggle('fast');
        $("."+contentClass).not($(this).next()).slideUp('fast');
    });
}

function showNotCompliedDrillDownRecord(data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();
    $(".escalation-drilldown-list .td-escalation").empty();
    $(".drilldown-title").text("Over due compliances of "+GROUP_NAME);
    var data =  data['drill_down_data'];
    var filter_type = chartInput.getFilterType();
    if(filter_type == "group"){
        groupWiseNotCompliedDrillDown("not_complied", data);
    }
    if(filter_type == "business_group"){
        businessgroupWiseNotCompliedDrillDown("not_complied", data);
    }
    if(filter_type == "legal_entity"){
        legalentityWiseNotCompliedDrillDown("not_complied", data);
    }
    if(filter_type == "division"){
        divisionWiseNotCompliedDrillDown("not_complied", data);
    }
    if(filter_type == "unit"){
        unitWiseNotCompliedDrillDown("not_complied", data);
    }
}
function groupWiseNotCompliedDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").show();
    $(".businessgroup-name").show();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();

    $(".tr-level1 th").attr("colspan", "8");
    $(".tr-unit .unit-heading").attr("colspan", "7");

    notCompliedDrilldown(status, data);
}

function businessgroupWiseNotCompliedDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();


    $(".tr-level1 th").attr("colspan", "7");
    $(".tr-unit .unit-heading").attr("colspan", "6");

    notCompliedDrilldown(status, data);
}
function legalentityWiseNotCompliedDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").show();
    $(".division-name").show();

    $(".tr-level1 th").attr("colspan", "6");
    $(".tr-unit .unit-heading").attr("colspan", "5");

    notCompliedDrilldown(status, data);
}

function divisionWiseNotCompliedDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();

    $(".tr-level1 th").attr("colspan", "5");
    $(".tr-unit .unit-heading").attr("colspan", "4");

    notCompliedDrilldown(status, data);

}

function unitWiseNotCompliedDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();

    $(".tr-level1 th").attr("colspan", "5");
    $(".tr-unit .unit-heading").attr("colspan", "4");

    notCompliedDrilldown(status, data);
}

function notCompliedDrilldown(status, data){
    $(".btn-back").on("click", function() {
        $(".graph-container.compliance-status").show();
        $(".drilldown-container").hide();
        loadNotCompliedChart();
    });

    var sno = 1;
    var count = 1;

    var tableHeading = $('#templates .notComplied-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);

    var tableFilter = $('#templates .notComplied-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-thead-drilldown-list").append(cloneFilter);

    $.each(data, function(key, value){
        var tableUnit = $('#templates .notComplied-status .tr-unit');
        var cloneUnit = tableUnit.clone();
        $(".unit-heading", cloneUnit).html(value["unit_name"]);
        $(".table-drilldown-list").append(cloneUnit);
        $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
        if(count==1){
            $('.accordion-content'+count).addClass("default");
        }
        var unitList = value["compliances"];

        $.each(unitList, function(ke, valu){
            var tableLevel1 = $('#templates .notComplied-status .tr-level1');
            var cloneLevel1 = tableLevel1.clone();
            $(".heading", cloneLevel1).html(ke);
            $('.accordion-content'+count).append(cloneLevel1);

            $.each(valu, function(k, val){
                var tableRow = $('#templates .notComplied-status .table-row-list');
                var clone = tableRow.clone();
                $(".sno", clone).html(sno);
                $(".businessgroup-name", clone).html(value["business_group"]);
                $(".legalentity-name", clone).html(value["legal_entity"])
                $(".division-name", clone).html(value["division"]);
                $(".industry-type-name", clone).html(value["industry_name"]);
                $(".compliance-name span", clone).html(val['compliance_name']);
                $(".assigned-to", clone).html(val['assignee_name']);
                $(".over-due", clone).html(val['ageing']);
                $('.accordion-content'+count).append(clone);
                sno = sno + 1;

            });
        });
        count = count + 1;
    });
    accordianType('accordion', 'accordion-toggle', 'accordion-content');
    $('.js-filtertable').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter');
    });

}

function showEscalationDrillDownRecord(data, year){
    $(".escalation-drilldown-list .td-escalation").empty();
    var filter_type = chartInput.getFilterType();
    $('.drilldown-title').text("Escalations of "+GROUP_NAME+" for the year "+year);
    if(filter_type == "group"){
        $(".table-thead-drilldown-list").empty();
        $(".table-drilldown-list tbody").remove();

        groupWiseEscalationDrillDown("delayed", data);
        groupWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "business_group"){
        $(".table-thead-drilldown-list").empty();
        $(".table-drilldown-list tbody").remove();

        businessgroupWiseEscalationDrillDown("delayed", data);
        businessgroupWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "legal_entity"){
        $(".table-thead-drilldown-list").empty();
        $(".table-drilldown-list tbody").remove();

        legalentityWiseEscalationDrillDown("delayed", data);
        legalentityWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "division"){
        $(".table-thead-drilldown-list").empty();
        $(".table-drilldown-list tbody").remove();

        divisionWiseEscalationDrillDown("delayed", data);
        divisionWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "unit"){
        $(".table-thead-drilldown-list").empty();
        $(".table-drilldown-list tbody").remove();

        unitWiseEscalationDrillDown("delayed", data);
        unitWiseEscalationDrillDown("not_complied", data);
    }
}
function groupWiseEscalationDrillDown(status, data){
    $(".business-group-row").show();
    $(".businessgroup-name").show();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();

    if (status == "not_complied") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".delayed-by-row").hide();
        $(".over-due-row").show();
    }
    else if (status == "delayed") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".delayed-by-row").show();
        $(".over-due-row").hide();
    }

    escalationDrilldown(status, data);
}
function businessgroupWiseEscalationDrillDown(status, data){
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();

    if (status == "not_complied") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".delayed-by-row").hide();
        $(".over-due-row").show();
    }
    else if (status == "delayed") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".delayed-by-row").show();
        $(".over-due-row").hide();
    }

    escalationDrilldown(status, data);
}
function legalentityWiseEscalationDrillDown(status, data){
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").show();
    $(".division-name").show();

    if (status == "not_complied") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".over-due-row").show();
        $(".delayed-by-row").hide();
    }
    else if (status == "delayed") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".delayed-by-row").show();
        $(".over-due-row").hide();
    }
    escalationDrilldown(status, data);
}

function divisionWiseEscalationDrillDown(status, data){
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();

    if (status == "not_complied") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".over-due-row").show();
        $(".delayed-by-row").hide();
    }
    else if (status == "delayed") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".delayed-by-row").show();
        $(".over-due-row").hide();
    }
    escalationDrilldown(status, data);
}

function unitWiseEscalationDrillDown(status, data){
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();

    if (status == "not_complied") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".over-due-row").show();
        $(".delayed-by-row").hide();
        var status = "Not Complied"
    }
    else if (status == "delayed") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".delayed-by-row").show();
        $(".over-due-row").hide();
        var status = "Delayed"
    }

    escalationDrilldown(status, data);
}

function escalationDrilldown(status, data){
    var sno = 1;
    var count = 1;
    
    if(status == "not_complied"){
        $(".escalation-drilldown-list .td-escalation").append('<table class="inner-table-notcomplied-escalation-list js-filtertable_not_c"><thead class="thead-itncel"></thead></table>');
        var h2heading = $('#templates .escalation-status .tr-h2');
        var cloneh2 = h2heading.clone();        
        $(".escalation-status-value", cloneh2).html("Not Complied compliances");        
        $(".thead-itncel").append(cloneh2);

        var tableHeading = $('#templates .escalation-status .tr-heading');
        var cloneHeading = tableHeading.clone();
        $(".thead-itncel").append(cloneHeading);

        var tableFilter = $('#templates .escalation-status .tr-filter');
        var cloneFilter = tableFilter.clone();
        $(".thead-itncel").append(cloneFilter);

        $(".inner-table-notcomplied-escalation-list .business-group-row .filter-text-box").addClass("js-filter_not_c");
        $(".inner-table-notcomplied-escalation-list .legal-entity-row .filter-text-box").addClass("js-filter_not_c");
        $(".inner-table-notcomplied-escalation-list .division-row .filter-text-box").addClass("js-filter_not_c");
        $(".inner-table-notcomplied-escalation-list .type-row .filter-text-box").addClass("js-filter_not_c");
        $(".inner-table-notcomplied-escalation-list .compliance-row .filter-text-box").addClass("js-filter_not_c");
        $(".inner-table-notcomplied-escalation-list .assigned-to-row .filter-text-box").addClass("js-filter_not_c");        
        $(".inner-table-notcomplied-escalation-list .over-due-row .filter-text-box").addClass("js-filter_not_c");

        if(data[status].length > 0){

            $.each(data[status], function(key, value){
                var tableUnit = $('#templates .escalation-status .tr-unit');
                var cloneUnit = tableUnit.clone();
                $(".unit-heading", cloneUnit).html(value["unit_name"]);
                $(".inner-table-notcomplied-escalation-list").append(cloneUnit);
                $('.inner-table-notcomplied-escalation-list').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
                if(count==1){
                    $('.accordion-content'+count).addClass("default");
                }
                var unitList = value["compliances"];

                $.each(unitList, function(ke, valu){
                    var tableLevel1 = $('#templates .escalation-status .tr-level1');
                    var cloneLevel1 = tableLevel1.clone();
                    $(".heading", cloneLevel1).html(ke);
                    $('.accordion-content'+count).append(cloneLevel1);

                    $.each(valu, function(k, val){
                        var tableRow = $('#templates .escalation-status .table-row-list');
                        var clone = tableRow.clone();
                        $(".sno", clone).html(sno);
                        $(".businessgroup-name", clone).html(value["business_group"]);
                        $(".legalentity-name", clone).html(value["legal_entity"])
                        $(".division-name", clone).html(value["division"]);
                        $(".industry-type-name", clone).html(value["industry_name"]);
                        $(".compliance-name span", clone).html(val['compliance_name']);
                        $(".assigned-to", clone).html(val['assignee_name']);

                        if(val['status'] == "Delayed Compliance"){
                            $(".delayed-by", clone).html(val['ageing']);
                        }
                        if(val['status'] == "Not Complied"){
                            $(".over-due", clone).html(val['ageing']);
                        }
                        $('.accordion-content'+count).append(clone);
                        sno = sno + 1;

                    });
                });
                count = count + 1;
            });

            accordianType('accordion', 'accordion-toggle', 'accordion-content');
        }
        else{
            var tableRow = $('#templates .escalation-status .norecords-list');
            var clone = tableRow.clone();
            $('.norecord', clone).html("No Record Found");
            $('.inner-table-notcomplied-escalation-list').append(clone);
        }
        $('.js-filtertable_not_c').on('keyup', function () {
            $(this).filtertable().addFilter('.js-filter_not_c');
        });
    }
    if(status == "delayed"){
        $(".escalation-drilldown-list .td-escalation").append('<table class="inner-table-delayed-escalation-list js-filtertable_delayed"><thead-itdel class="thead-itdel"></thead></table>');
        var h2heading = $('#templates .escalation-status .tr-h2');
        var cloneh2 = h2heading.clone();        
        $(".escalation-status-value", cloneh2).html("Delayed compliances");        
        $(".thead-itdel").append(cloneh2);

        var tableHeading = $('#templates .escalation-status .tr-heading');
        var cloneHeading = tableHeading.clone();
        $(".thead-itdel").append(cloneHeading);

        var tableFilter = $('#templates .escalation-status .tr-filter');
        var cloneFilter = tableFilter.clone();
        $(".thead-itdel").append(cloneFilter);

        $(".inner-table-delayed-escalation-list .business-group-row .filter-text-box").addClass("js-filter_delayed");
        $(".inner-table-delayed-escalation-list .legal-entity-row .filter-text-box").addClass("js-filter_delayed");
        $(".inner-table-delayed-escalation-list .division-row .filter-text-box").addClass("js-filter_delayed");
        $(".inner-table-delayed-escalation-list .type-row .filter-text-box").addClass("js-filter_delayed");
        $(".inner-table-delayed-escalation-list .compliance-row .filter-text-box").addClass("js-filter_delayed");
        $(".inner-table-delayed-escalation-list .assigned-to-row .filter-text-box").addClass("js-filter_delayed");        
        $(".inner-table-delayed-escalation-list .delayed-by-row .filter-text-box").addClass("js-filter_delayed");

        if(data[status].length > 0){

            $.each(data[status], function(key, value){
                var tableUnit = $('#templates .escalation-status .tr-unit');
                var cloneUnit = tableUnit.clone();
                $(".unit-heading", cloneUnit).html(value["unit_name"]);
                $(".inner-table-delayed-escalation-list").append(cloneUnit);
                $('.inner-table-delayed-escalation-list').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
                if(count==1){
                    $('.accordion-content'+count).addClass("default");
                }
                var unitList = value["compliances"];

                $.each(unitList, function(ke, valu){
                    var tableLevel1 = $('#templates .escalation-status .tr-level1');
                    var cloneLevel1 = tableLevel1.clone();
                    $(".heading", cloneLevel1).html(ke);
                    $('.accordion-content'+count).append(cloneLevel1);

                    $.each(valu, function(k, val){
                        var tableRow = $('#templates .escalation-status .table-row-list');
                        var clone = tableRow.clone();
                        $(".sno", clone).html(sno);
                        $(".businessgroup-name", clone).html(value["business_group"]);
                        $(".legalentity-name", clone).html(value["legal_entity"])
                        $(".division-name", clone).html(value["division"]);
                        $(".industry-type-name", clone).html(value["industry_name"]);
                        $(".compliance-name span", clone).html(val['compliance_name']);
                        $(".assigned-to", clone).html(val['assignee_name']);

                        if(val['status'] == "Delayed Compliance"){
                            $(".delayed-by", clone).html(val['ageing']);
                        }
                        if(val['status'] == "Not Complied"){
                            $(".over-due", clone).html(val['ageing']);
                        }
                        $('.accordion-content'+count).append(clone);
                        sno = sno + 1;

                    });
                });
                count = count + 1;
            });

            accordianType('accordion', 'accordion-toggle', 'accordion-content');
        }
        else{
            var tableRow = $('#templates .escalation-status .norecords-list');
            var clone = tableRow.clone();
            $('.norecord', clone).html("No Record Found");
            $('.inner-table-delayed-escalation-list').append(clone);
        }
        $('.js-filtertable_delayed').on('keyup', function () {
            $(this).filtertable().addFilter('.js-filter_delayed');
        });
    }
}

// Trend Chart Drill Down
function updateTrendChartDrillDown(status, data, year) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showTrendChartDrillDownRecord(status, data, year);
}

function showTrendChartDrillDownRecord(status, data, year){
    $(".drilldown-title").text("Trend Chart of the "+year);
    var data = data["drill_down_data"];
    var filter_type = chartInput.getFilterType();
    if(filter_type == "group"){
        groupWiseTrendChartDrillDown(status, data);
    }
    if(filter_type == "business_group"){
        businessgroupWiseTrendChartDrillDown(status, data);
    }
    if(filter_type == "legal_entity"){
        legalentityWiseTrendChartDrillDown(status, data);
    }
    if(filter_type == "division"){
        divisionWiseTrendChartDrillDown(status, data);
    }
    if(filter_type == "unit"){
        unitWiseTrendChartDrillDown(status, data);
    }
}

function groupWiseTrendChartDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").show();
    $(".businessgroup-name").show();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();

    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".over-due-row").show();
    }
    else if (status == "Delayed") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit tr th").attr("colspan", "6");
    }
    trendChartDrilldown(status, data);
}

function businessgroupWiseTrendChartDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();

    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".over-due-row").show();
    }
    else if (status == "Delayed") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit tr th").attr("colspan", "5");
    }
    trendChartDrilldown(status, data);
}

function legalentityWiseTrendChartDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").show();
    $(".division-name").show();

    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".over-due-row").show();
    }
    else if (status == "Delayed") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit tr th").attr("colspan", "4");
    }
    trendChartDrilldown(status, data);
}

function divisionWiseTrendChartDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();


    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".over-due-row").show();
    }
    else if (status == "Delayed") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "4");
        $(".tr-unit tr th").attr("colspan", "3");
    }
    trendChartDrilldown(status, data);

}

function unitWiseTrendChartDrillDown(status, data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();


    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".over-due-row").show();
    }
    else if (status == "Delayed") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "4");
        $(".tr-unit tr th").attr("colspan", "3");
    }
    trendChartDrilldown(status, data);
}

function trendChartDrilldown(status, data){
    var sno = 1;
    var count = 1;
    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-thead-drilldown-list").append(cloneFilter);
    $.each(data, function(key, value){
        var tableUnit = $('#templates .compliance-status .tr-unit');
        var cloneUnit = tableUnit.clone();
        $(".unit-heading", cloneUnit).html(value["unit_name"]);
        $(".table-drilldown-list").append(cloneUnit);
        $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
        if(count==1){
            $('.accordion-content'+count).addClass("default");
        }
        var unitList = value["compliances"];
        $.each(unitList, function(ke, valu){
            var tableLevel1 = $('#templates .compliance-status .tr-level1');
            var cloneLevel1 = tableLevel1.clone();
            $(".heading", cloneLevel1).html(ke);
            $('.accordion-content'+count).append(cloneLevel1);
            $.each(valu, function(k, val){
                var tableRow = $('#templates .compliance-status .table-row-list');
                var clone = tableRow.clone();
                $(".sno", clone).html(sno);
                $(".businessgroup-name", clone).html(value["business_group"]);
                $(".legalentity-name", clone).html(value["legal_entity"])
                $(".division-name", clone).html(value["division"]);
                $(".industry-type-name", clone).html(value["industry_name"]);
                $(".compliance-name span", clone).html(val['compliance_name']);
                $(".assigned-to", clone).html(val['assignee_name']);
                if(val['status'] == "Delayed"){
                    $(".delayed-by", clone).html(val['ageing']+" Days");
                }
                if(val['status'] == "Inprogress"){
                    $(".dates-left-to-complete", clone).html(val['ageing']+" Days");
                }
                if(val['status'] == "Not Complied"){
                    $(".over-due", clone).html(val['ageing']+" Days");
                }
                $('.accordion-content'+count).append(clone);
                sno = sno + 1;

            });
        });
        count = count + 1;
    });

    accordianType('accordion', 'accordion-toggle', 'accordion-content');
    $('.js-filtertable').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter');
    });
}

function accordianType(idtype, toggleClass, contentClass){
    $('#'+idtype).find('.'+toggleClass).click(function(){
        $(this).next().slideToggle('fast');
        $("."+contentClass).not($(this).next()).slideUp('fast');
    });
}




function showDrillDownRecord(status, data, filterTypeName){
    var data = data["drill_down_data"];
    var filter_type = chartInput.getFilterType();
    if(filter_type == "group"){
        groupWiseComplianceDrillDown(status, data);
        drilldownTitleText = "Compliances - Country: " +filterTypeName +", Status: "+status;
    }
    if(filter_type == "business_group"){
        businessgroupWiseComplianceDrillDown(status, data);
        drilldownTitleText = "Compliances - Business Group: " +filterTypeName +", Status: "+status;
    }
    if(filter_type == "legal_entity"){
        legalentityWiseComplianceDrillDown(status, data);
        drilldownTitleText = "Compliances - Legal Entity: " +filterTypeName +", Status: "+status;
    }
    if(filter_type == "division"){
        divisionWiseComplianceDrillDown(status, data);
        drilldownTitleText = "Compliances - Division: " +filterTypeName +", Status: "+status;
    }
    if(filter_type == "unit"){
        unitWiseComplianceDrillDown(status, data);
        drilldownTitleText = "Compliances - Unit: " +filterTypeName +", Status: "+status;
    }
    $('.drilldown-title').text(drilldownTitleText);
}

function groupWiseComplianceDrillDown(status, data){
    $(".table-drilldown-list thead").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").show();
    $(".businessgroup-name").show();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();

    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".over-due-row").show();
    }
    else if (status == "Delayed Compliance") {
        $(".tr-level1 th").attr("colspan", "8");
        $(".tr-unit .unit-heading").attr("colspan", "7");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit tr th").attr("colspan", "6");
    }
    complianceStatusDrilldown(status, data);
}

function businessgroupWiseComplianceDrillDown(status, data){
    $(".table-drilldown-list thead").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").show();
    $(".legalentity-name").show();

    $(".division-row").show();
    $(".division-name").show();

    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".over-due-row").show();
    }
    else if (status == "Delayed Compliance") {
        $(".tr-level1 th").attr("colspan", "7");
        $(".tr-unit .unit-heading").attr("colspan", "6");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit tr th").attr("colspan", "5");
    }
    complianceStatusDrilldown(status, data);
}

function legalentityWiseComplianceDrillDown(status, data){
    $(".table-drilldown-list thead").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").show();
    $(".division-name").show();

    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".over-due-row").show();
    }
    else if (status == "Delayed Compliance") {
        $(".tr-level1 th").attr("colspan", "6");
        $(".tr-unit .unit-heading").attr("colspan", "5");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit tr th").attr("colspan", "4");
    }
    complianceStatusDrilldown(status, data);
}

function divisionWiseComplianceDrillDown(status, data){
    $(".table-drilldown-list thead").empty();
    $(".table-drilldown-list tbody").remove();

    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();


    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".over-due-row").show();
    }
    else if (status == "Delayed Compliance") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "4");
        $(".tr-unit tr th").attr("colspan", "3");
    }
    complianceStatusDrilldown(status, data);
}

function unitWiseComplianceDrillDown(status, data){
    $(".table-drilldown-list thead").empty();
    $(".table-drilldown-list tbody").remove();
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

    $(".division-row").hide();
    $(".division-name").hide();


    $(".delayed-by-row").hide();
    $(".dates-left-to-complete-row").hide();
    $(".over-due-row").hide();

    if (status == "Inprogress") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".dates-left-to-complete-row").show();
    }
    else if (status == "Not Complied") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".over-due-row").show();
    }
    else if (status == "Delayed Compliance") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".delayed-by-row").show();
    }
    else{
        $(".tr-level1 th").attr("colspan", "4");
        $(".tr-unit tr th").attr("colspan", "3");
    }
    complianceStatusDrilldown(status, data);
}

function complianceStatusDrilldown(status, data){
    var sno = 1;
    var count = 1;
    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-thead-drilldown-list").append(cloneFilter);
    $.each(data, function(key, value){
        var tableUnit = $('#templates .compliance-status .tr-unit');
        var cloneUnit = tableUnit.clone();
        $(".unit-heading", cloneUnit).html(value["unit_name"]);
        $(".table-drilldown-list").append(cloneUnit);
        $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
        if(count==1){
            $('.accordion-content'+count).addClass("default");
        }
        var unitList = value["compliances"];
        $.each(unitList, function(ke, valu){
            var tableLevel1 = $('#templates .compliance-status .tr-level1');
            var cloneLevel1 = tableLevel1.clone();
            $(".heading", cloneLevel1).html(ke);
            $('.accordion-content'+count).append(cloneLevel1);
            $.each(valu, function(k, val){
                var tableRow = $('#templates .compliance-status .table-row-list');
                var clone = tableRow.clone();
                $(".sno", clone).html(sno);
                $(".businessgroup-name", clone).html(value["business_group"]);
                $(".legalentity-name", clone).html(value["legal_entity"])
                $(".division-name", clone).html(value["division"]);
                $(".industry-type-name", clone).html(value["industry_name"]);
                $(".compliance-name span", clone).html(val['compliance_name']);
                $(".assigned-to", clone).html(val['assignee_name']);
                if(val['status'] == "Delayed Compliance"){
                    $(".delayed-by", clone).html(val['ageing']);
                }
                if(val['status'] == "Inprogress"){
                    $(".dates-left-to-complete", clone).html(val['ageing']);
                }
                if(val['status'] == "Not Complied"){
                    $(".over-due", clone).html(val['ageing']);
                }
                $('.accordion-content'+count).append(clone);
                sno = sno + 1;

            });
        });
        count = count + 1;
    });

    accordianType('accordion', 'accordion-toggle', 'accordion-content');
    $('.js-filtertable').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter');
    });
}

function accordianType(idtype, toggleClass, contentClass){
    $('#'+idtype).find('.'+toggleClass).click(function(){
        $(this).next().slideToggle('fast');
        $("."+contentClass).not($(this).next()).slideUp('fast');
    });
}

//  Escalation Chart
function prepareEscalationChartdata(source_data) {
    var chartTitle = getFilterTypeTitle();
    var xAxis = [];

    function set_value(dict, key, value) {
        var temp = dict[key];
        if (typeof(temp) === "undefined")
            temp = 0;
        temp = parseInt(temp) + parseInt(value);
        dict[key] = temp;
    }
    chart_data = source_data.chart_data;

    var chartDataSeries = [];
    delayed_data = [];
    not_complied_data = [];
    $.each(chart_data, function(i, value) {
        delayed = value["delayed_compliance_count"];
        not_complied = value["not_complied_count"];
        year = value["year"];
        if  ((delayed == 0) && (not_complied == 0)) {

        }
        else {
            delayed_data.push({
                "y": delayed,
                "drilldown": "Delayed Compliance",
                "year": year
            });
            not_complied_data.push({
                "y": not_complied,
                "drilldown": "Not Complied",
                "year": year
            });
            xAxis.push(year);
        }
    });

    chartDataSeries.push({
        "name": "Delayed Compliance",
        "data": delayed_data
    });
    chartDataSeries.push(
        {
            "name": "Not Complied",
            "data": not_complied_data
        }
    );

    var filterTypeInput = getFilterTypeInput()
    if (chartTitle == "Country") {
        chartTitle = "Escalation of " + GROUP_NAME
    }
    else {
        filter_names = []
        for (var i=0; i < filterTypeInput.length; i++){
            name = getFilterTypeName(filterTypeInput[i]);
            filter_names.push(name);
        }
        chartTitle = "Escalation of " + chartTitle + " " + filter_names;
    }
    return [xAxis, chartDataSeries, chartTitle]
}

function updateEscalationChart(data) {
    $(".graph-container.compliance-status").show();
    data = prepareEscalationChartdata(data);
    xAxis = data[0];
    chartDataSeries = data[1];
    chartTitle = data[2];

    highchart = new Highcharts.Chart({
        colors:['#F58835','#F32D2B',],
        chart: {
            type: 'column',
            renderTo: "status-container",
            width: '850'
        },
        title: {
            text: chartTitle
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: xAxis,
            crosshair: true,
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total Compliances'
            },
            allowDecimals: false
        },
        plotOptions: {
            series: {
                pointWidth: 40,
                groupPadding: 0.4,
                pointPadding: -0.0,
                pointPlacement: -0.0
            },
            column: {
                dataLabels: {
                    enabled: true,
                    textShadow:null,
                    format:'{point.y}'
                },
            }
        },
        series: chartDataSeries,
    });
    $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
        var year = (this.textContent || this.innerText);
        loadEscalationDrillDown(year);
        // setChart(value);
    });
}

// Trend Chart

function prepareTrendChartData(source_data) {
    var chartTitle = getFilterTypeTitle();
    var xAxis = [];
    var xAxisIds = [];
    var chartDataSeries = [];
    xAxis = source_data["years"];
    for (var i =0; i< source_data["data"].length; i++) {
        chartData = source_data["data"][i];
        var filter_type_id = chartData["filter_id"];
        if (filterTypeInput.indexOf(filter_type_id) == -1)
            continue;
        var filterTypeName = getFilterTypeName(filter_type_id);

        compliance_count = [];
        total_count = [];
        compliance_info = chartData["complied_compliance"];
        data = []
        for (var j = 0; j < compliance_info.length; j++) {
            compliance_count.push(
                compliance_info[j]["complied_compliances_count"]
            );
            total_count.push(
                compliance_info[j]["total_compliances"]
            );
            data.push({
                y: compliance_info[j]["complied_compliances_count"],
                t: compliance_info[j]["total_compliances"]
            });

        }
        chartDataSeries.push(
            {
                "name": filterTypeName,
                "data": data,
                "total":total_count
            }
        );
    }
    chartTitle = "Complied (" + xAxis[0] + " to " + xAxis[xAxis.length - 1] + ")";
    return [xAxis, chartTitle, chartDataSeries];
}

function updateTrendChart(data) {
    data = prepareTrendChartData(data);
    xAxis = data[0];
    chartTitle = data[1];
    chartDataSeries = data[2];
    var highchart;
    highchart = new Highcharts.Chart({
        chart: {
            renderTo: "status-container",
        },
        title: {
            text: chartTitle
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: xAxis,
            title: {
                text: "Year",
            },
            labels: {
                style: {
                    cursor: 'pointer',
                    color: "blue",
                    textDecoration: "underline",
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Compliance (%)'
            },
            labels: {
                formatter: function() {
                    return this.value + '%';
                }
            },
            allowDecimals: false
        },
        tooltip: {
            crosshair: true,
            shared: true,
            backgroundColor: "#FCFFC5",
            headerFormat: '<b>{point.x}</b>: {point.percentage:.0f}% ',
            pointFormat: '({point.y} out of {point.stackTotal})',
            formatter: function() {
                var s = '<b>' + this.x + '</b>',
                sum = 0;
                $.each(this.points, function(i, point) {
                    total = point.point.t;
                    tasks = (point.y/100) * total;
                    color = point.color;
                    s += '<br/><span style="color:' + color + '"> <b>'+ point.series.name + '</b> </span>: ' + point.y + '% (' + Math.round(tasks)+ ' out of ' + total + ')';
                    sum += point.y;
                })
                return s;
            }
        },
        plotOptions: {
            spline: {
                marker: {
                    radius: 4,
                    lineColor: "#666666",
                    lineWidth: 1
                }
            }
        },
        series: chartDataSeries,

    });
    $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
        var value = (this.textContent || this.innerText);
        name = value;

        loadTrendChartDrillDown(value);
        $(".btn-back").show();
        $(".btn-back").on("click", function() {
            updateTrendChart(data);
            $(".btn-back").hide();
        });

        // setChart(value);
    });
}

function prepareNotCompliedChart(source_data) {
    var chartTitle = getFilterTypeTitle();
    var chartDataSeries = [];
    count = 0;
    $.each(source_data, function(key, item) {
        count += item;
        if (key == "T_31_to_60_days_count") {
            chartDataSeries.push(
                {
                    name: "Below 60",
                    y: item,
                    drilldown: "Below 60"
                }
            );
        }
        else if (key == "T_0_to_30_days_count") {
            chartDataSeries.push(
                {
                    name: "Below 30",
                    y: item,
                    drilldown: "Below 30"
                }
            );
        }
        else if (key == "T_61_to_90_days_count") {
            chartDataSeries.push(
                {
                    name: "Below 90",
                    y: item,
                    drilldown: "Below 90"
                }
            )
        }
        else if (key == "Above_90_days_count") {
            chartDataSeries.push(
                {
                    name: "Above 90",
                    y: item,
                    drilldown: "Above 90"
                }
            )
        }
    });
    if (count == 0)
        chartDataSeries = [];
    var filterTypeInput = getFilterTypeInput()
    if (chartTitle == "Country") {
        chartTitle = "Over due compliance of " + GROUP_NAME
    }
    else {
        filter_names = []
        for (var i=0; i < filterTypeInput.length; i++){
            name = getFilterTypeName(filterTypeInput[i]);
            filter_names.push(name);
        }
        chartTitle = "Over due compliance of " + chartTitle + " " + filter_names;
    }
    return [chartDataSeries, chartTitle,  count];
}

function updateNotCompliedChart(data) {
    data = prepareNotCompliedChart(data);
    chartDataSeries = data[0];
    chartTitle = data[1];
    total = data[2];
    highchart = new Highcharts.Chart({
        colors: ['#FF9C80', '#F2746B', '#FB4739', '#DD070C'],
        chart: {
            renderTo: "status-container",
            type: "pie",
            options3d: {
                enabled: true,
                alpha: 30
            }
        },
        title: {
            text: chartTitle
        },
        xAxis: {
            categories: true,
        },
        credits: {
            enabled: false
        },
        tooltip: {
            headerFormat: '',
            pointFormat: '<span>{point.name} days</span>: <b>{point.y:.0f}</b>out of total' + total
        },
        legend: {
            enabled: true
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 45,
                dataLabels: {
                    enabled: true,
                    format: '{point.percentage: .0f}%'
                },
                showInLegend: true,
                point: {
                    events: {
                        click: function() {
                            var drilldown = this.drilldown
                            loadNotCompliedDrillDown(drilldown);
                        }
                    }
                }
            },
        },
        series: [{
            name: "compliance",
            colorByPoint: true,
            data: chartDataSeries
        }],
    });
}

function prepareComplianceApplicability(source_data) {
    chartDataSeries = [];
    chartTitle = getFilterTypeTitle();
    applicable = source_data["applicable_count"];
    not_applicable = source_data["not_applicable_count"];
    not_opted = source_data["not_opted_count"];
    if (
        (applicable == 0) &&
        (not_applicable == 0) &&
        (not_opted == 0)
    ) {
        //pass
    }
    else {
        chartDataSeries.push({
            name: "Applicable",
            y: applicable,
            drilldown: "Applicable"
        });
        chartDataSeries.push({
            name: "Not Applicable",
            y: not_applicable,
            drilldown: "Not Applicable"
        });
        chartDataSeries.push({
            name: "Not Opted",
            y: not_opted,
            drilldown: "Not Applicable"
        });
    }
    var filterTypeInput = getFilterTypeInput()
    if (chartTitle == "Country") {
        chartTitle = "Compliance Applicability Status of " + GROUP_NAME
    }
    else {
        filter_names = []
        for (var i=0; i < filterTypeInput.length; i++){
            name = getFilterTypeName(filterTypeInput[i]);
            filter_names.push(name);
        }
        chartTitle = "Compliance Applicability Status of " + chartTitle + " " + filter_names;
    }
    return [chartDataSeries, chartTitle]

}

function updateComplianceApplicabilityChart(data) {
    data = prepareComplianceApplicability(data);
    chartTitle = data[1];
    chartDataSeries = data[0];
    highchart = new Highcharts.Chart({
        colors: ['#66FF66','#FFDC52','#CE253C'],
        chart: {
            type: "pie",
            renderTo: "status-container",
            options3d: {
                enabled: true,
                alpha: 45
            }
        },
        title: {
            text: chartTitle
        },
        xAxis: {
            categories: true,
        },
        credits: {
            enabled: false
        },
        tooltip: {
            headerFormat: '',
            pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f}</b>out of total'
        },
        legend: {
            enabled: true
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 40,
                dataLabels: {
                    enabled: true,
                    format: '{point.percentage: .0f}%'
                },
                showInLegend: true,
                point: {
                    events: {
                        click: function() {
                            var drilldown = this.drilldown
                            loadComplianceApplicabilityDrillDown(drilldown);
                        }
                    }
                }
            },
        },
        series: [{
            name: "compliance",
            colorByPoint: true,
            data : chartDataSeries
        }],
    });
}

function updateAssigneeWiseComplianceFiltersList(data)
{
    $(".table-assignee-wise-compliance-list").hide();
    $(".grid-table-dash1").hide();
    $('.popupoverlay').css("visibility","hidden");
    $('.popupoverlay').css("opacity","0");
    COUNTRYLIST = data['countries'];
    BUSINESSGROUPSLIST = data['business_groups'];
    LEGALENTITYLIST = data['legal_entities'];
    DIVISIONLIST = data['divisions'];
    UNITLIST = data['units'];
    USERLIST = data['users'];
}

function showFiltersResults() {
    var country = $("#country").val().trim();
    var countryval = $("#countryval").val().trim();
    if(countryval == ""){
        displayMessage("Country Required");
    }
    var businessgroupid = parseInt($("#businessgroupid").val());
    var businessgroupsval = $("#businessgroupsval").val().trim();
    if(businessgroupsval == ""){
        businessgroupid = null
    }
    var legalentityid = parseInt($("#legalentityid").val().trim());
    var legalentityval = $("#legalentityval").val().trim();
    if(legalentityval == "" ){
        legalentityid = null
    }
    var divisionid = parseInt($("#divisionid").val().trim());
    var divisionval = $("#divisionval").val().trim();
    if(divisionval == ""){
        divisionid = null
    }
     var unitid = parseInt($("#unitid").val().trim());
    var unitval = $("#unitval").val().trim();
    if(unitval == ""){
        unitid = null
    }
    var userid = parseInt($("#userid").val().trim());
    var userval = $("#userval").val().trim();
    if(userval == ""){
        userid = null
    }
    client_mirror.getAssigneewiseComplianes(
        parseInt(country), businessgroupid, legalentityid,
        divisionid, unitid, userid,
        function (status, data) {
            updateAssigneeWiseComplianceList(data['chart_data']);
        }
    );

}

function updateAssigneeWiseComplianceList(data){
    $('.tbody-assignee-wise-compliance-list tr').remove();
    $('.compliance-details-drilldown tr').remove();
    $(".table-assignee-wise-compliance-list").show();
    var sno = 0;

    $.each(data, function(key, value) {
        var tableRowHeadingth = $('#templates .assignee-wise-compliance-list .unitHeading');
        var cloneHeadingth = tableRowHeadingth.clone();
        $('.unit-name', cloneHeadingth).text(value['unit_name']);
        $('.tbody-assignee-wise-compliance-list').append(cloneHeadingth);

        var assigneewiselist = value['assignee_wise_details'];
        $.each(assigneewiselist, function(ke, valu) {
            var tableRow = $('#templates .assignee-wise-compliance-list .userHeading ');
            var clone = tableRow.clone();
            $('.assignee-name-for-popup', clone).html(valu['assignee_name']);
            $(clone, ".assignee-name-for-popup").on("click", function(e){
                $("#popup-year").show();
                showPopup(assigneewiselist);
            });
            $('.tbody-assignee-wise-compliance-list').append(clone);

            var list = valu['domain_wise_details'];
            $.each(list, function(k, val){
                var domainArr = [];
                var tableRowvalues = $('#templates .assignee-wise-compliance-list .assignee-row-list');
                var cloneval = tableRowvalues.clone();
                sno = sno + 1;
                $('.sno', cloneval).text(sno);
                $('.level1value', cloneval).html(val['domain_name']);
                $('.total-count', cloneval).html(val['total_compliances']);
                $('.complied-count', cloneval).html(val['complied_count']);
                if(val['delayed_compliance']['reassigned_count'] == 0){
                    $('.delayed-count', cloneval).html(val['delayed_compliance']['assigned_count']);
                    $(cloneval, ".delayed-count").on("click", function(e){
                        $("#popup-reassigned").show();
                        showPopupCompDelayed(reassignedlist);
                    });
                }
                else{
                    var delayvalue = val['delayed_compliance']['assigned_count']+"("+val['delayed_compliance']['reassigned_count']+")";
                    $('.delayed-count', cloneval).html(delayvalue);
                    $('.delayed-count', cloneval).addClass("delayedvalue");
                    $(cloneval, ".delayedvalue").on("click", function(e){
                        showComplianceNotifications(val['delayed_compliance']['reassigned_compliances']);
                    });
                }

                $('.inprogress-count', cloneval).html(val['inprogress_compliance_count']);
                $('.not-complied-count', cloneval).html(val['not_complied_count']);
                $(cloneval, ".assign-wise-compliance-details").on("click", function(e){
                    showComplianceList();
                });
                domainArr = val['domain_id'];
                var year = null;
                $(cloneval, ".assignee-row-list").on("click", function(e){
                    updateComplianceList(valu['user_id'], domainArr, year );
                });
                $('.tbody-assignee-wise-compliance-list').append(cloneval);
            });
        });

    });
}
function showComplianceList(reassigned_compliances){
    $('.popupoverlay').css("visibility","visible");
    $('.popupoverlay').css("opacity","1");
}
function updateComplianceList(userid, domainid, year){
    $('.popupoverlay').css("visibility","hidden");
    $('.popupoverlay').css("opacity","0");
    $(".table-assignee-wise-compliance-list").hide();
    $(".grid-table-dash1").show();
    client_mirror.getAssigneewiseCompliancesDrilldown(
        userid, domainid, year,
        function (status, data) {
            listingCompliance(data, userid, year);
        }
    );
}
function getDomainName(doaminId){
    var domainName;
    $.each(DOMAINLIST, function (key, value){
        if(value['domain_id'] == doaminId){
            domainName = value['domain_name'];
            return false;
        }
    });
    return domainName;
}
function getUserName(userid){
    var userName;
    $.each(USERLIST, function (key, value){
        if(value['employee_id'] == userid){
            userName = value['employee_name'];
            return false;
        }
    });
    return userName;
}
function listingCompliance(data, userid, year){
    $('.tbody-assignee-wise-compliance-list tr').remove();
    $('.compliance-details-drilldown tr').remove();

    $(".table-assignee-wise-compliance-list").show();
    var sno = 0;

    $.each(data, function(key, value) {
        var tableRowHeadingth = $('#templates .compliance-details-list .filterHeader');
        var cloneHeadingth = tableRowHeadingth.clone();
        $('.comp-list-user', cloneHeadingth).text(getUserName[userid]);
        $('.comp-list-year', cloneHeadingth).text(year);
        $('.comp-list-filter-domain', cloneHeadingth).hide();
        $('.compliance-details-drilldown').append(cloneHeadingth);

        var statuswiselist = value;
        $.each(statuswiselist, function(ke, valu) {
            var tableRow = $('#templates .compliance-details-list .comp-list-statusheading ');
            var clone = tableRow.clone();
            $('.comp-list-status', clone).html(ke);
            $('.compliance-details-drilldown').append(clone);

            var tableRowheading = $('#templates .compliance-details-list .comp-list-heading');
            var cloneHeading = tableRowheading.clone();
            $('.compliance-details-drilldown').append(cloneHeading);

            var list = valu;
            $.each(list, function(k, val){
                var tableRowunits = $('#templates .compliance-details-list .comp-list-filter-unitname');
                var cloneunits = tableRowunits.clone();
                $('.comp-list-unitname', cloneunits).html(val['unit_name']);
                $('.compliance-details-drilldown').append(cloneunits);

                var complianceslist = val['compliances'];
                $.each(complianceslist, function(k1, v1){
                    var tableRowLevel1 = $('#templates .compliance-details-list .comp-list-level1');
                    var cloneLevel1 = tableRowLevel1.clone();
                    $(".comp-list-level1-val", cloneLevel1).text(k1)
                    $(".compliance-details-drilldown").append(cloneLevel1);
                    $.each(v1, function(k2, v2){
                        var tableRowvalues = $('#templates .compliance-details-list .comp-list-tablerowlist');
                        var cloneval = tableRowvalues.clone();
                        sno = sno + 1;
                        $('.comp-list-sno', cloneval).text(sno);
                        $('.comp-list-compliance', cloneval).html(v2['compliance_name']);
                        $('.comp-list-startdate', cloneval).text(v2['assigned_date']);
                        $('.comp-list-duedate', cloneval).text(v2['due_date']);
                        $('.comp-list-completiondate', cloneval).text(v2['completion_date']);
                        $('.compliance-details-drilldown').append(cloneval);
                    });
                });
            });
        });

    });

}
function showPopup(assigneewiselist){
    $.each(assigneewiselist, function(ke, valu) {
        $('.popupoverlay').css("visibility","visible");
        $('.popupoverlay').css("opacity","1");
        var popupsno = 0;
        var domainArr = [];
        var userid = valu['user_id'];
        var domainWiseDetails = valu['domain_wise_details'];
        $.each(domainWiseDetails, function(key, value){
            domainArr.push(value['domain_id']);
        });
        var yearWiseDetails = valu['year_wise_details'];
        $.each(yearWiseDetails, function(k, val){
            var tableRow = $('#templates .year-wise-compliance-list-popup .tablerow');
            var cloneval = tableRow.clone();
            popupsno = popupsno + 1;
            $('.popup-sno', cloneval).text(popupsno);
            $('.popup-year-val', cloneval).html(val['year']);
            $('.popup-total-count', cloneval).html(val['total_compliances']);
            $('.popup-complied-count', cloneval).html(val['complied_count']);
            $('.popup-delayed-count', cloneval).html(val['delayed_compliance']);
            $('.popup-inprogress-count', cloneval).html(val['inprogress_compliance_count']);
            $('.popup-not-complied-count', cloneval).html(val['not_complied_count']);
            $(".popup-click-drilldown", cloneval).on("click", function(){
                updateComplianceList(userid, domainArr, parseInt(val['year']));
            });
            $('.tbody-popup-list').append(cloneval);
        });
    });
}
function showPopupCompDelayed(reassignedlist){
    $.each(reassignedlist, function(ke, valu) {
        $('.popupoverlay').css("visibility","visible");
        $('.popupoverlay').css("opacity","1");
        var popupdelayedsno = 0;
        $.each(reassignedlist, function(k, val){
            var tableRow = $('#templates .comp-list-delayed-row-list');
            var cloneval = tableRow.clone();
            popupdelayedsno = popupdelayedsno + 1;
            $('.comp-delayed-sno', cloneval).text(popupdelayedsno);
            $('.comp-delayed-compliance', cloneval).html(val['compliance']);
            $('.comp-delayed-reassigned-from', cloneval).html(val['reassigned_from']);
            $('.comp-delayed-startdate', cloneval).html(val['start_date']);
            $('.comp-delayed-duedate', cloneval).html(val['due_date']);
            $('.comp-delayed-reassigned-date', cloneval).html(val['reassigned_from']);
            $('.comp-delayed-completed-date', cloneval).html(val['completion_date']);           
            $('.tbody-popup-reassigned-list').append(cloneval);
        });
    });
}

function close(){
    $('.popupoverlay').css("visibility","hidden");
    $('.popupoverlay').css("opacity","0");
}

//Chart load function

function loadComplianceStatusChart () {
    var requestData = parseComplianceStatusApiInput();
    client_mirror.getComplianceStatusChartData(
        requestData,
        function (status, data) {
            // TODO: API Error Validation
            COMPLIANCE_STATUS_DATA = data["chart_data"];
            data = data["chart_data"];
            //console.log(COMPLIANCE_STATUS_DATA)
            updateComplianceStatusChart(data.splice(0, 7));

            hideLoader();
        }
    );
}

function loadComplianceStatusDrillDown(compliance_status, filter_type_id, filter_type_name) {
    $(".btn-bar-chart").hide();
    $(".btn-pie-chart").hide();
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    requestData = {
        "domain_ids": chartInput.getDomains(),
        "from_date": chartInput.getFromDate(),
        "to_date": chartInput.getToDate(),
        "filter_type": filterType,
        "filter_id": filter_type_id,
        "compliance_status": compliance_status,
        "year": chartInput.getCurrentYear()
    }
    $(".btn-back").on("click", function() {
        loadComplianceStatusChart();
    });
    client_mirror.getComplianceStatusDrillDown(
        requestData,
        function (status, data) {
            COMPLIANCE_STATUS_DRILL_DOWN_DATE = data;
            updateDrillDown(compliance_status, data, filter_type_name);
        }
    );
}

function loadEscalationDrillDown(year) {
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == "Group") {
        filter_ids = chartInput.getCountries();
    }
    else {
        filter_ids = getFilterIds(filter_type);
    }
    var requestData = {
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": filter_ids,
        "year": parseInt(year)
    }
    $(".btn-back").on("click", function() {
        loadEscalationChart();
    });
    client_mirror.getEscalationDrillDown(
        requestData,
        function (status, data) {
            ESCALATION_STATUS_DRILL_DOWN_DATA = data;
            updateEscalationDrillDown(data, year);
        }
    );
}

function loadEscalationChart() {
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == "Group") {
        filter_ids = chartInput.getCountries();
    }
    else {
        filter_ids = getFilterIds(filter_type);
    }
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": filter_ids
    };
    client_mirror.getEscalationChartData(
        requestData,
        function (status, data) {
            ESCALATION_DATA = data;
            updateEscalationChart(data);
        }
    )
}

function loadTrendChart(){
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": [1]
    };
    client_mirror.getTrendChart(
        requestData, function(status, data) {
            TREND_CHART_DATA = data;
            updateTrendChart(data);
        }
    )
}

function loadTrendChartDrillDown(year){
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": [1],
        "year": parseInt(year)
    };
    $(".btn-back").on("click", function() {
        loadTrendChart();
    });
    client_mirror.getTrendChartDrillDown(
        requestData, function(status, data) {
            TREND_CHART_DATA = data;
            updateTrendChartDrillDown(status, data, year);
        }
    )
}

function loadNotCompliedChart(){
    var filter_type = chartInput.getFilterType();
    var filter_ids = getFilterIds(filter_type);
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == "Group") {
        filter_ids = chartInput.getCountries();
    }
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": filter_ids
    };
    client_mirror.getNotCompliedData(
        requestData, function(status, data) {
            NOT_COMPLIED_DATA = data;
            updateNotCompliedChart(data);
        }
    );
}

function loadNotCompliedDrillDown(type){
    var filter_type = chartInput.getFilterType();
    var filter_ids = getFilterIds(filter_type);
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == "Group") {
        filter_ids = chartInput.getCountries();
    }
    var requestData = {
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": filter_ids,
        "not_complied_type": type
    }
    client_mirror.getNotCompliedDrillDown(
        requestData,
        function (status, data) {
            NOT_COMPLIED_DRILL_DOWN_DATA = data;
            updateNotCompliedDrillDown(status, data);
        }
    );
}

function loadComplianceApplicabilityChart(){
    var filter_type = chartInput.getFilterType();
    var filter_ids = getFilterIds(filter_type);

    var filter_type = chartInput.getFilterType().replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filter_type)
    if (filterType == "Group") {
        filter_ids = chartInput.getCountries();
    }
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": filter_ids
    };
    client_mirror.getComplianceApplicabilityChart(
        requestData, function(status, data) {
            COMPLIANCE_APPLICABILITY_DATA = data;
            updateComplianceApplicabilityChart(data);
        }
    );
}

function loadComplianceApplicabilityDrillDown(type){

    var filter_type = chartInput.getFilterType();
    filter_ids = getFilterIds(filter_type)
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    if (filterType == "Group") {
        filter_ids = chartInput.getCountries();
    }
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": filter_ids,
        "applicability_status": type
    }
    $(".btn-back").on("click", function() {
        $(".graph-container.compliance-status").show();
        $(".drilldown-container").hide();
        loadComplianceApplicabilityChart();
    });
    client_mirror.getComplianceApplicabilityDrillDown(
        requestData,
        function (status, data) {
            COMPLIANCE_APPLICABILITY_DRILL_DOWN = data;
            updateComplianceApplicabilityDrillDown(status, data, type);
        }
    );
}


function loadAssigneeWiseCompliance() {
    client_mirror.getAssigneewiseComplianesFilters(
        function(status, data) {
            updateAssigneeWiseComplianceFiltersList(data);
        }
    );
}

function loadCharts () {
    // displayLoader();
    hideButtons();
    $(".drilldown-container").hide();
    $(".graph-container.compliance-status").show();
    var chartType = chartInput.getChartType();
    chartInput.setChartYear(0);
    if (chartType == "compliance_report") {
        $(".chart-container-inner").hide();
        $(".report-container-inner").show();
    }
    else {
        if (chartType == "compliance_status") {
            $(".chart-filters").show();
            $(".chart-filters-autocomplete").hide();
            $(".graph-selections-bottom").show();
            $("#DateSelection").show();
            $(".btn-consolidated").show();
        }
        else {
            $(".chart-filters").show();
            $(".chart-filters-autocomplete").hide();
            $(".graph-selections-bottom").hide();
            $("#DateSelection").hide();
            $(".btn-consolidated").hide();
        }
        $(".chart-container-inner").show();
        $(".report-container-inner").hide();
    }
    if (chartType == "compliance_status") {
        loadComplianceStatusChart();
    }
    else if (chartType == "escalations") {
        loadEscalationChart();
    }
    else if (chartType == "not_complied") {
        loadNotCompliedChart();
    }
    else if (chartType == "compliance_report") {
        loadAssigneeWiseCompliance();
    }
    else if (chartType == "trend_chart") {
        loadTrendChart();
    }
    else if (chartType == "applicability_status") {
        loadComplianceApplicabilityChart();
    }
    else if (chartType == "assignee_wise_compliance") {
        loadAssignessWiseComplianceChart();
    }
    else {
        hideLoader();
    }
}


//
// initialize
//

function initializeChartTabs () {
    $(".chart-tab").on("click", function () {
        $(".chart-filter").removeClass("active");
        $(".filtertable .selections").hide();
        $(".btn-group").addClass("active");
        chartInput.setFilterType("group");
        $(".chart-tab").removeClass("active");
        if ($(this).hasClass("compliance-status-tab")) {
            $(".chart-tab.compliance-status-tab").addClass("active");
            chartInput.setChartType("compliance_status");
            loadSubFilters(selectall=true, singleSelect=false);
        }
        else if($(this).hasClass("escalations-tab")) {
            $(".chart-tab.escalations-tab").addClass("active");
            chartInput.setChartType("escalations");
            loadSubFilters(selectall=false, singleSelect=true);
        }
        else if($(this).hasClass("not-complied-tab")) {
            $(".chart-tab.not-complied-tab").addClass("active");
            chartInput.setChartType("not_complied");
            loadSubFilters(selectall=false, singleSelect=true);
        }
        else if($(this).hasClass("compliance-report-tab")) {
            $(".chart-tab.compliance-report-tab").addClass("active");
            chartInput.setChartType("compliance_report");
        }
        else if($(this).hasClass("trend-chart-tab")) {
            $(".chart-tab.trend-chart-tab").addClass("active");
            chartInput.setChartType("trend_chart");
            loadSubFilters(selectall=false, singleSelect=true);
        }
        else if($(this).hasClass("applicability-status-tab")) {
            $(".chart-tab.applicability-status-tab").addClass("active");
            chartInput.setChartType("applicability_status");
            loadSubFilters(selectall=false, singleSelect=true);
        }
        // if ($(this).hasClass("active")) {
        //     $(".chart-tab").removeClass("active");

        //     $(".chart-tab.compliance-status-tab").addClass("active");

        // }
        // $(".chart-tab").removeClass("active");
        // $(this).addClass("active");
        loadCharts();
    });
}

function loadCountries () {
    countries = CHART_FILTERS_DATA.countries
    for (var i = 0; i < countries.length; i++) {
        var country = countries[i];
        var option = getOptionElement(
            country["country_id"],
            country["country_name"],
            true
        );
        $('.country-filter').append(option);
    };
}

function loadDomains () {
    domains = CHART_FILTERS_DATA.domains;
    for (var i = 0; i < domains.length; i++) {
        var domain = domains[i];
        var option = getOptionElement(
            domain["domain_id"],
            domain["domain_name"],
            true
        );
        $('.domain-filter').append(option);
    };
}

function loadBusinessGroups (isSelectAll) {
    business_groups = CHART_FILTERS_DATA.business_groups;
    for (var i = 0; i < business_groups.length; i++) {
        var business_group = business_groups[i];
        var option = getOptionElement(
            business_group["business_group_id"],
            business_group["business_group_name"],
            isSelectAll
        );
        $('.bg-filter').append(option);
    };
    if (business_groups.length == 0) {
        $(".btn-business-group").hide();
    }
}

function loadLegalEntities (isSelectAll) {
    legal_entities = CHART_FILTERS_DATA.legal_entities;
    for (var i = 0; i < legal_entities.length; i++) {
        var legal_entity = legal_entities[i];
        var option = getOptionElement(
            legal_entity["legal_entity_id"],
            legal_entity["legal_entity_name"],
            isSelectAll
        );
        $('.legal-entity-filter').append(option);
    };
}

function loadDivisions (isSelectAll) {
    divisions = CHART_FILTERS_DATA.divisions;
    for (var i = 0; i < divisions.length; i++) {
        var division = divisions[i];
        var option = getOptionElement(
            division["division_id"],
            division["division_name"],
            isSelectAll
        );
        $('.division-filter').append(option);
    };
    if (divisions.length == 0) {
        $(".btn-division").hide();
    }
}

function loadUnits (isSelectAll) {

    $('.unit-filter').empty();
    units = CHART_FILTERS_DATA.units;

    for (var i = 0; i < units.length; i++) {
        var unit = units[i];
        var option = getOptionElement(
            unit["unit_id"],
            unit["unit_name"],
            isSelectAll
        );
        $('.unit-filter').append(option);
    };
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
        placeholder: "Select Business Group",
        onClick: function (business_group) {
            chartInput.setBusinessGroups(business_group.value, business_group.checked);
        },
        onCheckAll: function () {
            business_groups = get_ids(
                CHART_FILTERS_DATA.business_groups, "business_group_id"
            );
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
        placeholder: "Select Legal Entity",
        onClick: function (legal_entity) {
            chartInput.setLegalEntities(legal_entity.value, legal_entity.checked);
        },
        onCheckAll: function () {
            legal_entities = get_ids(
                CHART_FILTERS_DATA.legal_entities, "legal_entity_id"
            );
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
        placeholder: "Select Division",
        onClick: function (division) {
            chartInput.setDivisions(division.value, division.checked);
        },
        onCheckAll: function () {
            divisions = get_ids(CHART_FILTERS_DATA.divisions, "division_id");
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
        placeholder: "Select Unit",
        onClick: function (unit) {
            chartInput.setUnits(unit.value, unit.checked, isSingleSelect);
        },
        onCheckAll: function () {
            units = get_ids(CHART_FILTERS_DATA.units, "unit_id");
            chartInput.setUnitsAll(units);
        },
        onUncheckAll: function () {
            chartInput.setUnitsAll([]);
        }
    });
}

function initializeFilters () {
    loadCountries();
    $('.country-filter').multipleSelect({
        filter: true,
        placeholder: "Select Country",
        onClick: function (country) {
            chartInput.setCountries(country.value, country.checked);
        },
        onCheckAll: function () {
            countries = get_ids(CHART_FILTERS_DATA.countries, "country_id");
            chartInput.setCountriesAll(countries);
        },
        onUncheckAll: function () {
            chartInput.setCountriesAll([]);
        }
    });

    loadDomains();
    $('.domain-filter').multipleSelect({
        filter: true,
        placeholder: "Select Domain",
        onClick: function (domain) {
            chartInput.setDomains(domain.value, domain.checked);
        },
        onCheckAll: function () {
            domains = get_ids(CHART_FILTERS_DATA.domains, "domain_id");
            chartInput.setDomainsAll(domains);
        },
        onUncheckAll: function () {
            chartInput.setDomainsAll([]);
        }
    });

    loadSubFilters(selectall=true, singleSelect=false);

    $(".btn-country").on("click", function () {
        $(this).toggleClass("active");
        if ($(this).hasClass("active")) {
            chartInput.setCountrySelected(true);
            $('.country-selection').show();
        }
        else {
            chartInput.setCountrySelected(false);
            $('.country-selection').hide();
        }
    });

    $(".btn-domain").on("click", function () {
        $(this).toggleClass("active");
        if ($(this).hasClass("active")) {
            chartInput.setDomainSelected(true);
            $('.domain-selection').show();
        }
        else {
            chartInput.setDomainSelected(false);
            $('.domain-selection').hide();
        }
    });

    $(".btn-date").on("click", function () {
        $(this).toggleClass("active");
        if ($(this).hasClass("active")) {
            chartInput.setDateSelected(true);
            $('.date-selection').show();
        }
        else {
            chartInput.setDateSelected(false);
            $('.date-selection').hide();
        }
    });

    $(".btn-date-filter").on("click", function () {
        chartInput.setFromDate($("#fromdate").val());
        chartInput.setToDate($("#todate").val());
        loadCharts();
    });

    $(".chart-filter").on("click", function () {
        if ($(this).hasClass("active"))
            return;
        $(".chart-filter").removeClass("active");
        $(this).addClass("active");
        var filter_type = $(this).attr('class').split(" ")[1];
        filter_type = filter_type.replace("btn-", "");
        filter_type = filter_type.replace("-", "_");
        chartInput.setFilterType(filter_type);

        $(".filtertable .selections").hide();
        if (filter_type in ["group", "consolidated"])
            return;
        var filter_type_selection = filter_type.replace("_", "-") + "-selection";
        $("." + filter_type_selection).show();
        var chart_type = chartInput.getChartType();
        if (chart_type == "compliance_status") {
            loadCharts();
        }
        else {
            if (filter_type == "group") {
                loadCharts();
            }
        }
    });

    $(".common-filter .btn-go input").on("click", function () {
        var chart_type = chartInput.getChartType();
        loadCharts()
        // if (chart_type == "compliance_status") {
        //     updateCharts();
        // }
        // else {
        //     loadCharts();
        // }
    });

    $(".specific-filter .btn-go input").on("click", function () {
        loadCharts();
    });

    $(".btn-previous-year").on("click", function(event) {
        event.preventDefault();
        event.stopPropagation();
        currentYear = chartInput.getCurrentYear();
        chartYear = chartInput.getChartYear();
        if (chartYear == 0) {
            chartInput.setChartYear(currentYear - 1);
        } else {
            chartInput.setChartYear(chartYear - 1);
        }
        loadComplianceStatusChart()
    });

    $(".btn-next-year").on("click", function() {
        currentYear = chartInput.getCurrentYear();
        chartYear = chartInput.getChartYear();
        chartInput.setChartYear(chartYear + 1);
        loadComplianceStatusChart()
    });

    $(".btn-next").on("click", function() {
        range = chartInput.getRangeIndex();
        var data = [];
        if (range == 7) {
            data1 = COMPLIANCE_STATUS_DATA;
            data = data1.splice(0, range);
        }
        else {
            chartInput.setRangeIndex(7);
            data1 = COMPLIANCE_STATUS_DATA;
            data = data1.splice(range, range+7);
        }
        updateComplianceStatusChart(data);
    });
    $(".btn-previous").on("click", function() {
        range = chartInput.getRangeIndex();
        var data = [];
        if (range == 7) {
            data1 = COMPLIANCE_STATUS_DATA;
            data = data1.splice(0, range);
        }
        else {
            chartInput.setRangeIndex(range - 7);
            data1 = COMPLIANCE_STATUS_DATA;
            data = data1.splice(range-7, range);
        }
        updateComplianceStatusChart(data);
    });

}


function initializeCharts () {
    initializeFilters();
    initializeChartTabs();
    // loadSubFilters(selectall=true, singleSelect=false);
    // initializeComplianceStatusChart();
}

function toDict (target, list, id_key, value_key) {
    for (var i = 0; i < list.length; i++) {
        var item = list[i];
        target[item[id_key]] = item[value_key];
    };
}



$(document).ready(function () {

    hideLoader();
    if (!client_mirror.verifyLoggedIn()) {
        hideLoader();
        // window.location.href = "/login";
        return;
    }

    // client_mirror.checkContractExpiration(function (status, data) {
    //         if (data == null) {
    //             return
    //             $(".contract_timer_container").hide()
    //         }else{
    //             no_of_days_left = data.no_of_days_left
    //             $(".contract_timer_container").show()
    //             if (no_of_days_left <= 30){
    //                 $(".contract_timer").html(
    //                     "Contract Expires in "+no_of_days_left+" days"
    //                 )
    //             }
    //             else{
    //                 // alert("Contract not expired yet"+no_of_days_left)
    //             }
    //             notification_count = data.notification_count;
    //             console.log("notification_count"+notification_count);
    //             reminder_count = data.reminder_count;
    //             escalation_count = data.escalation_count;
    //             $("#notification_count").text(notification_count);
    //             $("#reminder_count").text(reminder_count);
    //             $("#escalation_count").text(escalation_count);
    //         }
    //     }
    // )

    client_mirror.getChartFilters(function (status, data) {
        if (data == null) {
            return
        }
        CHART_FILTERS_DATA = data;
        toDict(COUNTRIES, data.countries, "country_id", "country_name");
        toDict(DOMAINS, data.domains, "domain_id", "domain_name");
        toDict(
            BUSINESS_GROUPS, data.business_groups,
            "business_group_id", "business_group_name"
        );
        toDict(
            LEGAL_ENTITIES, data.legal_entities,
            "legal_entity_id", "legal_entity_name"
        );
        toDict(DIVISIONS, data.divisions, "division_id", "division_name");
        toDict(UNITS, data.units, "unit_id", "unit_name");
        DOMAIN_INFO = data.domain_info;
        GROUP_NAME = data.group_name;
        initializeCharts();

        loadCharts();
    });

    $("#fromdate" ).datepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    });
    $( "#todate" ).datepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    });
});


//Assignee Wise Compliance list - autocomplete for all fields
function hidecountrylist(){
    document.getElementById('autocompleteview-country').style.display = 'none';
}
function loadauto_country (textval) {
    document.getElementById('autocompleteview-country').style.display = 'block';
    var countries = COUNTRYLIST;
    var suggestions = [];
    $('#autocompleteview-country ul').empty();
    if(textval.length>0){
        for(var i in countries){
          if (~countries[i]['country_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]);
        }
        var str='';
        for(var i in suggestions){
          str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-country ul').append(str);
        $("#country").val('');
    }
}
function activate_text (element,checkval,checkname) {
    $("#countryval").val(checkname);
    $("#country").val(checkval);
}

//Business Groups---------------------------------------------------------------------------------------------------------------
function hidebgroupslist(){
    document.getElementById('autocompleteview-bgroups').style.display = 'none';
}
function loadauto_businessgroups (textval) {
    if($("#businessgroupsval").val() == ''){
        $("#businessgroupid").val('');
    }
    document.getElementById('autocompleteview-bgroups').style.display = 'block';
    var bgroups = BUSINESSGROUPSLIST;
    var suggestions = [];
    $('#autocompleteview-bgroups ul').empty();
    if(textval.length>0){
        for(var i in bgroups){
            if (~bgroups[i]['business_group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([bgroups[i]["business_group_id"],bgroups[i]["business_group_name"]]);
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'" onclick="activate_businessgroups(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-bgroups ul').append(str);
        $("#businessgroupid").val('');
    }
}
function activate_businessgroups (element,checkval,checkname) {
  $("#businessgroupsval").val(checkname);
  $("#businessgroupid").val(checkval);
}
//Legal Entity---------------------------------------------------------------------------------------------------------------
function hidelentitylist(){
    document.getElementById('autocompleteview-lentity').style.display = 'none';
}
function loadauto_lentity (textval) {
    if($("#legalentityval").val() == ''){
        $("#legalentityid").val('');
    }
  document.getElementById('autocompleteview-lentity').style.display = 'block';
  var lentity = LEGALENTITYLIST;
  var suggestions = [];
  $('#autocompleteview-lentity ul').empty();
  if(textval.length>0){
    for(var i in lentity){
        if($("#businessgroupid").val()!=''){
            if (~lentity[i]['legal_entity_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]);
        }
        else{
         if (~lentity[i]['legal_entity_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]);
        }
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_lentity(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-lentity ul').append(str);
    $("#legalentityid").val('');
    }
}
function activate_lentity (element,checkval,checkname) {
  $("#legalentityval").val(checkname);
  $("#legalentityid").val(checkval);
}
//Division---------------------------------------------------------------------------------------------------------------
function hidedivisionlist(){
    document.getElementById('autocompleteview-division').style.display = 'none';
}
function loadauto_division (textval) {
    if($("#divisionval").val() == ''){
        $("#divisionid").val('');
    }
  document.getElementById('autocompleteview-division').style.display = 'block';
  var division = DIVISIONLIST;
  var suggestions = [];
  $('#autocompleteview-division ul').empty();
  if(textval.length>0){
    for(var i in division){
        if (~division[i]['division_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([division[i]["division_id"],division[i]["division_name"]]);
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_division(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-division ul').append(str);
    $("#divisionid").val('');
    }
}
function activate_division (element,checkval,checkname) {
  $("#divisionval").val(checkname);
  $("#divisionid").val(checkval);
}

//Units---------------------------------------------------------------------------------------------------------------
function hideunitlist(){
    document.getElementById('autocompleteview-unit').style.display = 'none';
}
function loadauto_unit (textval) {
    if($("#unitval").val() == ''){
        $("#unitid").val('');
    }
  document.getElementById('autocompleteview-unit').style.display = 'block';
  var unit = UNITLIST;
  var suggestions = [];
  $('#autocompleteview-unit ul').empty();
  if(textval.length>0){
    for(var i in unit){
        var getunitidname = unit[i]['unit_code']+"-"+unit[i]['unit_name'];
        if (~getunitidname.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"],unit[i]["unit_code"]]);
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_unit(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+suggestions[i][2]+'\')">'+suggestions[i][2]+'-'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-unit ul').append(str);
    $("#unitid").val('');
    }
}
function activate_unit (element,checkval,checkname, concatunit) {
  $("#unitval").val(concatunit+'-'+checkname);
  $("#unitid").val(checkval);
}


//USer---------------------------------------------------------------------------------------------------------------
function hideuserlist(){
    document.getElementById('autocompleteview-user').style.display = 'none';
}
function loadauto_user (textval) {
    if($("#userval").val() == ''){
        $("#userid").val('');
    }
  document.getElementById('autocompleteview-user').style.display = 'block';
  var users = USERLIST;
  var suggestions = [];
  $('#autocompleteview-user ul').empty();
  if(textval.length>0){
    for(var i in users){
        if (~users[i]['employee_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([users[i]["employee_id"],users[i]["employee_name"]]);
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_user(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-user ul').append(str);
    $("#userid").val('');
    }
}
function activate_user(element,checkval,checkname) {
  $("#userval").val(checkname);
  $("#userid").val(checkval);
}
