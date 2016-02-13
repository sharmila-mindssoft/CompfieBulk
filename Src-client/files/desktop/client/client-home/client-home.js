var CHART_FILTERS_DATA = null;
var COUNTRIES = {};
var BUSINESS_GROUPS = {};
var LEGAL_ENTITIES = {};
var DIVISIONS = {};
var UNITS = {};
var COMPLIANCE_STATUS_DATA = null;
var COMPLIANCE_STATUS_DRILL_DOWN_DATE = null;

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
    var chart_year = chartInput.getCurrentYear();
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

function prepareComplianceStatusChartData (source_data) {
    // var currentYear = (new Date()).getFullYear();
    var yearInput = chartInput.getCurrentYear()
    // var yearInput = currentYear - chartInput.getChartYear();
    // console.log(yearInput)
    var chartTitle = getFilterTypeTitle()
    var domainsInput = chartInput.getDomains();
    var xAxis = [];
    var xAxisIds = [];
    var yAxisComplied = [];
    var yAxisDelayed = [];
    var yAxisInprogress = [];
    var yAxisNotComplied = [];
    for (var i = 0; i < source_data.chart_data.length; i++) {
        var chartData = source_data.chart_data[i];
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
    console.log(chartTitle)
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
                "drilldown": yAxis[x1]
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
                events: {
                    click: function() {
                        setChart(this.value)
                    }
                },
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
            renderTo: "status-container",
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
                              console.log(drilldown)
                            }
                        }
                    }
                }
            },
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',

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

function updateDrillDown(data) {
    $(".graph-container.compliance-status").hide();
    $(".graph-selections-bottom").hide();
    $(".drilldown-container").show();
    $(".btn-back").show();
}

function loadComplianceStatusChart () {
    var requestData = parseComplianceStatusApiInput();
    client_mirror.getComplianceStatusChartData(
        requestData,
        function (status, data) {
            // TODO: API Error Validation
            COMPLIANCE_STATUS_DATA = data;
            updateComplianceStatusChart(data);
            hideLoader();
        }
    );
}

function loadComplianceStatusDrillDown(status, filter_type_id) {
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    requestData = {
        "domain_ids": chartInput.getDomains(),
        "from_date": chartInput.getFromDate(),
        "to_date": chartInput.getToDate(),
        "filter_type": filterType,
        "filter_id": filter_type_id,
        "compliance_status": status,
        "year": chartInput.getCurrentYear()
    }
    client_mirror.getComplianceStatusDrillDown(
        requestData,
        function (status, data) {
            COMPLIANCE_STATUS_DRILL_DOWN_DATE = data;
            updateDrillDown(data);
        }
    );
    console.log(status)
    console.log(filter_type_id)
}

function loadCharts () {
    // displayLoader();
    var chartType = chartInput.getChartType();
    if (chartType == "compliance_status") {
        loadComplianceStatusChart();
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
        if ($(this).hasClass("active")) {
            $(".chart-tab").removeClass("active");
            $(".chart-tab.compliance-status-tab").addClass("active");

        }
        $(".chart-tab").removeClass("active");
        $(this).addClass("active");
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
}

function initializeComplianceStatusChart () {
    // body...
}

function initializeCharts () {
    initializeFilters();
    initializeChartTabs();
    initializeComplianceStatusChart();
}

function toDict (target, list, id_key, value_key) {
    for (var i = 0; i < list.length; i++) {
        var item = list[i];
        target[item[id_key]] = item[value_key];
    };
}

$(document).ready(function () {
    if (!client_mirror.verifyLoggedIn()) {
        hideLoader();
        // window.location.href = "/login";
        return;
    }
    client_mirror.getChartFilters(function (status, data) {
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
