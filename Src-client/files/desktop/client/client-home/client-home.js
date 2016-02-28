var CHART_FILTERS_DATA = null;
var COUNTRIES = {};
var BUSINESS_GROUPS = {};
var LEGAL_ENTITIES = {};
var DIVISIONS = {};
var UNITS = {};

var COMPLIANCE_STATUS_DATA = null;
var COMPLIANCE_STATUS_DRILL_DOWN_DATE = null;

var ESCALATION_DATA = null;
var ESCALATION_STATUS_DRILL_DOWN_DATA = null;

var TREND_CHART_DATA = null;
var NOT_COMPLIED_DATA = null;
var NOT_COMPLIED_DRILL_DOWN_DATA = null;

var COMPLIANCE_APPLICABILITY_DATA = null;
var COMPLIANCE_APPLICABILITY_DRILL_DOWN = null;


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
        option.attr("selected");
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
        if (index > 0 && !isAdd) {
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
        else
            return get_ids(CHART_FILTERS_DATA.countries, "country_id");
    }

    this.setDomainSelected = function (v) {
        this.domain_selected = v;
    }

    this.setDomains = function (domain_id, isAdd) {
        domain_id = parseInt(domain_id);
        index = this.domains.indexOf(domain_id)
        if (index > 0 && !isAdd) {
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
        else
            return get_ids(CHART_FILTERS_DATA.domains, "domain_id");
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
        if (index > 0 && !isAdd) {
            this.business_groups.splice(index, 1);
            return;
        }
        if (isAdd) {
            this.business_groups.push(v);
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
        if (index > 0 && !isAdd) {
            this.legal_entities.splice(index, 1);
            return;
        }
        if (isAdd) {
            this.legal_entities.push(v);
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
        if (index > 0 && !isAdd) {
            this.divisions.splice(index, 1);
            return;
        }
        if (isAdd) {
            this.divisions.push(v);
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

    this.setUnits = function (v, isAdd) {
        v = parseInt(v);
        index = this.units.indexOf(v)
        if (index > 0 && !isAdd) {
            this.units.splice(index, 1);
            return;
        }
        if (isAdd) {
            this.units.push(v);
        }
    }

    this.setUnitsAll = function (units) {
        this.units = copyArray(units);
    }

    this.getUnits = function () {
        if (this.units.length > 0)
            return copyArray(this.units);
        else {
            if (this.filter_type == "unit")
                return get_ids(
                    CHART_FILTERS_DATA.units, "unit_id"
                );
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
    if (filter_type == "business_group")
        filterIds = chartInput.getBusinessGroups();
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
        return "Legal Entitiy";
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
            if (!(item["domain_id"] in domainsInput))
                continue;
            if (!(item["country_id"] in countriesInput))
                continue;
            compliedCount += item["complied_count"];
            delayedCount += item["delayed_compliance_count"];
            inprogressCount += item["inprogress_compliance_count"];
            notCompliedCount += item["not_complied_count"];
        };

        xAxis.push(filterTypeName);
        xAxisIds.push(filter_type_id);
        yAxisComplied.push(compliedCount);
        yAxisDelayed.push(delayedCount);
        yAxisInprogress.push(inprogressCount);
        yAxisNotComplied.push(notCompliedCount);
    };
    if (xAxis.length == 0)
        return null;
    var xAxisName = getXAxisName();
    var yAxis = ["Complied", "Delay Compliance", "Inprogress", "Not Complied"];
    var yAxisData = [
        yAxisComplied, yAxisDelayed, yAxisInprogress, yAxisNotComplied
    ];
    console.log("chartTitle = "+chartTitle);
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

    return [xAxisName, xAxis, chartDataSeries, chartTitle, xAxisDrillDownSeries];
}

function updateComplianceStatusChart (data) {
    var data = prepareComplianceStatusChartData(data);
    if (data == null)
        return;
    console.log("updateComplianceStatusChart")
    chartType = getFilterTypeTitle();
    if (chartType == "Consolidated") {
        chartTitle = "Consolidated Chart";
        updateComplianceStatusPieChart(data, chartTitle, "pie")
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
    var yAxisname = ["Complied", "Delay Compliance", "Inprogress", "Not Complied"];

    var highchart;
    function setChart(name) {
        data_series = drilldownSeries[name];
        var title = chartTitle + " - " + name;
        updateComplianceStatusPieChart(data_series, title, "pie");
        complianceDrillDown(data_series, title);
    }
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
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total compliances'
            },
            allowDecimals: false
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b>: {point.percentage:.0f}% ',
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
                                console.log(drilldown)
                                loadComplianceStatusDrillDown(drilldown, this.filter_type_id);
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
        console.log(value);
        name = value;
        data_series = drilldownSeries[name];
        var title = chartTitle + " - " + name;
        updateComplianceStatusPieChart(data_series, title, "pie");
        complianceDrillDown(data_series, title);
        // setChart(value);
    });
}

function complianceDrillDown(data_list, chartTitle) {
    $(".btn-bar-chart").on("click", function () {
        updateComplianceStatusPieChart(data_list, chartTitle, "column");
    });
    $(".btn-pie-chart").on("click", function () {
        updateComplianceStatusPieChart(data_list, chartTitle, "pie");
    });
}

function updateComplianceStatusPieChart(data_list, chartTitle, chartType) {
    var total = 0;
    for (var i=0; i < data_list.length; i++) {
        item = data_list[i];
        total += parseInt(item["y"]);
    }
    var options = {
    // var options = new Highcharts.Chart({
        colors:['#A5D17A','#F58835', '#F0F468', '#F32D2B'],
        chart: {
            renderTo: "status-container"
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
            column: {
                colorByPoint: true,
                point: {
                    events: {
                        click: function() {
                            var drilldown = this.drilldown;
                            if (drilldown) {
                              console.log(drilldown);
                              loadComplianceStatusDrillDown(this.name, this.filter_id)
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
                              console.log(drilldown)
                              console.log(this.name)
                              console.log(this.filter_id)
                              loadComplianceStatusDrillDown(this.name, this.filter_id)
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
            alpha: 30
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

function updateDrillDown(status, data) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showDrillDownRecord(status, data);
}

function updateEscalationDrillDown(status, data) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showDrillDownRecord(status, data);
}

function updateNotCompliedDrillDown(status, data) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showDrillDownRecord(status, data);
}

function updateComplianceApplicabilityDrillDown(status, data) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showDrillDownRecord(status, data);
}

function updateTrendChartDrillDown(status, data) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
    showDrillDownRecord(status, data);
}


function showDrillDownRecord(status, data){
    var data = data["drill_down_data"];
    var filter_type = chartInput.getFilterType();
    if(filter_type == "group"){
        groupWiseComplianceDrillDown(status, data);
    }
    if(filter_type == "business_group"){
        businessgroupWiseComplianceDrillDown(status, data);
    }
    if(filter_type == "legalentity"){
        legalentityWiseComplianceDrillDown(status, data);
    }
    if(filter_type == "division"){
        divisionWiseComplianceDrillDown(status, data);
    }
    if(filter_type == "unit"){
        unitWiseComplianceDrillDown(status, data);
    }
}

function groupWiseComplianceDrillDown(status, data){
    $(".table-drilldown-list tbody").remove();
    var sno;
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

    var sno = 1;
    var count = 1;
    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-drilldown-list").append(cloneFilter);
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

    $(document).ready(function($) {
        $('#accordion').find('.accordion-toggle').click(function(){
            $(this).next().slideToggle('fast');
            $(".accordion-content").not($(this).next()).slideUp('fast');
        });
    });
}

function businessgroupWiseComplianceDrillDown(status, data){
    $(".table-drilldown-list tbody").remove();
    var sno;
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

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
    var sno = 1;
    var count = 1;
    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-drilldown-list").append(cloneFilter);
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
    $(document).ready(function($) {
        $('#accordion').find('.accordion-toggle').click(function(){
            $(this).next().slideToggle('fast');
            $(".accordion-content").not($(this).next()).slideUp('fast');
        });
    });
}

function legalentityWiseComplianceDrillDown(data){
    $(".table-drilldown-list tbody").remove();
    var sno;
    $(".business-group-row").hide();
    $(".businessgroup-name").hide();

    $(".legal-entity-row").hide();
    $(".legalentity-name").hide();

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
    var sno = 1;
    var count = 1;
    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-drilldown-list").append(cloneFilter);
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
    $(document).ready(function($) {
        $('#accordion').find('.accordion-toggle').click(function(){
            $(this).next().slideToggle('fast');
            $(".accordion-content").not($(this).next()).slideUp('fast');
        });
    });
}

function divisionWiseComplianceDrillDown(data){
    $(".table-drilldown-list tbody").remove();
    var sno;
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
    var sno = 1;
    var count = 1;
    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-drilldown-list").append(cloneFilter);
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
    $(document).ready(function($) {
        $('#accordion').find('.accordion-toggle').click(function(){
            $(this).next().slideToggle('fast');
            $(".accordion-content").not($(this).next()).slideUp('fast');
        });
    });
}

function unitWiseComplianceDrillDown(data){
}

//  Escalation Chart
function prepareEscalationChartdata(source_data) {
    var chartTitle = getFilterTypeTitle();
    var domainsInput = chartInput.getDomains();
    var countriesInput = chartInput.getCountries();
    var xAxis = [];
    var yAxisDelayed = {}; //{ "year": count}
    var yAxisNotComplied = {};
    var filterTypeInput = getFilterTypeInput()
    function set_value(dict, key, value) {
        var temp = dict[key];
        if (typeof(temp) === "undefined")
            temp = 0;
        temp = parseInt(temp) + parseInt(value);
        dict[key] = temp;
    }
    for (var i = 0; i < source_data.chart_data.length; i++) {
        var chartData = source_data.chart_data[i];
        var filter_type_id = chartData["filter_type_id"];
        if (filterTypeInput.indexOf(filter_type_id) == -1)
            continue;
        // var filterTypeName = getFilterTypeName(filter_type_id);
        for (var j = 0; j < chartData["data"].length; j++) {
            var item = chartData["data"][j];
            if (domainsInput.indexOf(item["domain_id"]) == -1)
                continue;
            if(countriesInput.indexOf(item["country_id"]) == -1)
                continue;
            year = item["year"];
            if (
                (item["delayed_compliance_count"] !== 0) ||
                (item["not_complied_count"] !== 0)
            ){
                set_value(yAxisDelayed, year, item["delayed_compliance_count"]);
                set_value(yAxisNotComplied, year, item["not_complied_count"]);
                if (xAxis.indexOf(year) == -1)
                    xAxis.push(year);
            }
        }

    }
    if (xAxis.length == 0)
        return null;
    var chartDataSeries = [];
    delayed_data = []
    $.each(yAxisDelayed, function(key, value) {
        delayed_data.push({
            "y": value,
            "drilldown":"Delay Compliance",
            "year": key
        });
    });
    not_complied_data = [];
    $.each(yAxisNotComplied, function(key, value) {
        not_complied_data.push({
            "y": value,
            "drilldown":"Not Complied",
            "year": key
        });
    });
    chartDataSeries.push({
        "name": "Delay Compliance",
        "data": delayed_data
    });
    chartDataSeries.push(
        {
            "name": "Not Complied",
            "data": not_complied_data
        }
    );
    console.log(chartDataSeries)
    chartTitle = "Escalation of " + chartTitle;
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
        },
        title: {
            text: chartTitle
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
                pointWidth: 40
            },
            column: {
                pointPadding: 0,
                groupPadding: 0.3,
                borderWidth: 0,
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
        console.log(year);
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
    console.log(xAxis)
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
        console.log(total_count)
        chartDataSeries.push(
            {
                "name": filterTypeName,
                "data": data,
                "total":total_count
            }
        );
    }
    console.log(chartDataSeries)
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
        console.log(value);
        name = value;
        loadTrendChartDrillDown(value);

        // setChart(value);
    });
}

function prepareNotCompliedChart(source_data) {
    var chartTitle = getFilterTypeTitle();
    var chartDataSeries = [];
    $.each(source_data, function(key, item) {
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
    return [chartDataSeries, chartTitle];
}

function updateNotCompliedChart(data) {
    data = prepareNotCompliedChart(data);
    chartDataSeries = data[0];
    chartTitle = data[1];
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
            text: 'Over due compliance of' + chartTitle
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
                            console.log(drilldown);
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
    chartTitle = "Compliance Applicability Status";
    chartDataSeries.push({
        name: "Applicable",
        y: source_data["applicable_count"],
        drilldown: "Applicable"
    });
    chartDataSeries.push({
        name: "Not Applicable",
        y: source_data["not_applicable_count"],
        drilldown: "Not Applicable"
    });
    chartDataSeries.push({
        name: "Not Opted",
        y: source_data["not_opted_count"],
        drilldown: "Not Applicable"
    });
    return [chartDataSeries, chartTitle]

}

function updateComplianceApplicabilityChart(data) {
    data = prepareComplianceApplicability(data);
    chartTitle = data[1];
    chartDataSeries = data[0];
    console.log(chartDataSeries)
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
                            console.log(drilldown);
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

//Chart load function

function loadComplianceStatusChart () {
    var requestData = parseComplianceStatusApiInput();
    console.log(requestData);
    client_mirror.getComplianceStatusChartData(
        requestData,
        function (status, data) {
            // TODO: API Error Validation
            data = data["chart_data"];
            COMPLIANCE_STATUS_DATA = data;
            updateComplianceStatusChart(data.splice(0, 7));
            hideLoader();
        }
    );
}

function loadComplianceStatusDrillDown(compliance_status, filter_type_id) {
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
    console.log(requestData)
    client_mirror.getComplianceStatusDrillDown(
        requestData,
        function (status, data) {
            COMPLIANCE_STATUS_DRILL_DOWN_DATE = data;
            updateDrillDown(compliance_status, data);
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
    console.log(requestData);
    client_mirror.getEscalationDrillDown(
        requestData,
        function (status, data) {
            ESCALATION_STATUS_DRILL_DOWN_DATA = data;
            console.log(data);
            updateEscalationDrillDown(data);
        }
    );
}

function loadEscalationChart() {
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_id": 1
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
            console.log(data)
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
    client_mirror.getTrendChartDrillDown(
        requestData, function(status, data) {
            TREND_CHART_DATA = data;
            console.log(data)
            updateTrendChartDrillDown(status, data);
        }
    )
}

function loadNotCompliedChart(){
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_id": 1
    };
    client_mirror.getNotCompliedData(
        requestData, function(status, data) {
            NOT_COMPLIED_DATA = data;
            console.log(data)
            updateNotCompliedChart(data);
        }
    );
}

function loadNotCompliedDrillDown(type){
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
        "not_complied_type": type
    }
    console.log(requestData);
    client_mirror.getNotCompliedDrillDown(
        requestData,
        function (status, data) {
            NOT_COMPLIED_DRILL_DOWN_DATA = data;
            console.log(data);
            updateNotCompliedDrillDown(status, data);
        }
    );
}

function loadComplianceApplicabilityChart(){
    var filter_type = chartInput.getFilterType().replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filter_type)
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_id": 1
    };
    client_mirror.getComplianceApplicabilityChart(
        requestData, function(status, data) {
            COMPLIANCE_APPLICABILITY_DATA = data;
            console.log(data);
            updateComplianceApplicabilityChart(data);
        }
    );
}

function loadComplianceApplicabilityDrillDown(type){
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
        "filter_id": filter_ids[0],
        "applicability_status": type
    }
    console.log(requestData);
    client_mirror.getComplianceApplicabilityDrillDown(
        requestData,
        function (status, data) {
            COMPLIANCE_APPLICABILITY_DRILL_DOWN = data;
            console.log(data);
            updateComplianceApplicabilityDrillDown(status, data);
        }
    );
}


function loadAssigneeWiseCompliance() {

}

function loadCharts () {
    // displayLoader();
    hideButtons();
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
        }
        else {
            $(".chart-filters").show();
            $(".chart-filters-autocomplete").show();
            $(".graph-selections-bottom").hide();
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
    else {
        hideLoader();
    }
}


//
// initialize
//

function initializeChartTabs () {
    $(".chart-tab").on("click", function () {
        $(".chart-tab").removeClass("active");
        if ($(this).hasClass("compliance-status-tab")) {
            $(".chart-tab.compliance-status-tab").addClass("active");
            chartInput.setChartType("compliance_status");
        }
        else if($(this).hasClass("escalations-tab")) {
            $(".chart-tab.escalations-tab").addClass("active");
            chartInput.setChartType("escalations");
        }
        else if($(this).hasClass("not-complied-tab")) {
            $(".chart-tab.not-complied-tab").addClass("active");
            chartInput.setChartType("not_complied");
        }
        else if($(this).hasClass("compliance-report-tab")) {
            $(".chart-tab.compliance-report-tab").addClass("active");
            chartInput.setChartType("compliance_report");
        }
        else if($(this).hasClass("trend-chart-tab")) {
            $(".chart-tab.trend-chart-tab").addClass("active");
            chartInput.setChartType("trend_chart");
        }
        else if($(this).hasClass("applicability-status-tab")) {
            $(".chart-tab.applicability-status-tab").addClass("active");
            chartInput.setChartType("applicability_status");
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
            country["country_id"], country["country_name"]
        );
        $('.country-filter').append(option);
    };
}

function loadDomains () {
    domains = CHART_FILTERS_DATA.domains;
    for (var i = 0; i < domains.length; i++) {
        var domain = domains[i];
        var option = getOptionElement(
            domain["domain_id"], domain["domain_name"]
        );
        $('.domain-filter').append(option);
    };
}

function loadBusinessGroups () {
    business_groups = CHART_FILTERS_DATA.business_groups;
    for (var i = 0; i < business_groups.length; i++) {
        var business_group = business_groups[i];
        var option = getOptionElement(
            business_group["business_group_id"],
            business_group["business_group_name"]
        );
        $('.bg-filter').append(option);
    };
}

function loadLegalEntities () {
    legal_entities = CHART_FILTERS_DATA.legal_entities;
    for (var i = 0; i < legal_entities.length; i++) {
        var legal_entity = legal_entities[i];
        var option = getOptionElement(
            legal_entity["legal_entity_id"], legal_entity["legal_entity_name"]
        );
        $('.legal-entity-filter').append(option);
    };
}

function loadDivisions () {
    divisions = CHART_FILTERS_DATA.divisions;
    for (var i = 0; i < divisions.length; i++) {
        var division = divisions[i];
        var option = getOptionElement(
            division["division_id"], division["division_name"]
        );
        $('.division-filter').append(option);
    };
}

function loadUnits () {
    $('.unit-filter').empty();
    units = CHART_FILTERS_DATA.units;
    for (var i = 0; i < units.length; i++) {
        var unit = units[i];
        var option = getOptionElement(
            unit["unit_id"], unit["unit_name"]
        );
        $('.unit-filter').append(option);
    };
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

    loadBusinessGroups();
    $('.bg-filter').multipleSelect({
        filter: true,
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

    loadLegalEntities();
    $('.legal-entity-filter').multipleSelect({
        filter: true,
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

    loadDivisions();
    $('.division-filter').multipleSelect({
        filter: true,
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

    loadUnits();
    $('.unit-filter').multipleSelect({
        filter: true,
        placeholder: "Select Unit",
        onClick: function (unit) {
            chartInput.setUnits(unit.value, unit.checked);
        },
        onCheckAll: function () {
            units = get_ids(CHART_FILTERS_DATA.units, "unit_id");
            chartInput.setUnitsAll(units);
        },
        onUncheckAll: function () {
            chartInput.setUnitsAll([]);
        }
    });

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
        loadCharts();
    });

    $(".common-filter .btn-go input").on("click", function () {
        updateCharts();
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
        console.log(chartInput.getChartYear())
        console.log("previous_year");
        loadComplianceStatusChart()
    });

    $(".btn-next-year").on("click", function() {
        currentYear = chartInput.getCurrentYear();
        chartYear = chartInput.getChartYear();
        chartInput.setChartYear(chartYear + 1);
        console.log(chartInput.getChartYear());
        console.log("next_year");
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
        console.log("data");
        console.log(data)
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
        console.log("data");
        console.log(data)
    });

}


function initializeCharts () {
    initializeFilters();
    initializeChartTabs();
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
    client_mirror.getChartFilters(function (status, data) {
        console.log(data)
        if (data == null) {
            return
        }
        CHART_FILTERS_DATA = data;
        toDict(COUNTRIES, data.countries, "country_id", "country_name");
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
        initializeCharts();
        loadCharts();
    });
});
