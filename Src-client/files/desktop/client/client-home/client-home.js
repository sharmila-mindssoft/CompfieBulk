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

var PAGESIZE = 500;
var STARTCOUNT = 0;
var ENDCOUNT;
var SNO = 0;
var FULLARRAYLIST = [];
var ACCORDIONCOUNT = 0;
var ACCORDIONCOUNTNC = 0;
var ACCORDIONCOUNTD = 0;
var RECORDCOUNT  = 0;

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


var chartInput = new ChartInput();

//  Compliance Status Chart

function updateComplianceStatusChart (data_input) {
    var data = prepareComplianceStatusChartData(data_input);
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
        },
        title: {
            text: chartTitle
        },
        credits: {
            enabled: false
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
                depth: 35,
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
            alpha: 55,
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

    showComplianceApplicabilityDrillDownRecord_set(data, type);
}
function showComplianceApplicabilityDrillDownRecord_set(data, type){
    $(".level-heading").attr("colspan", "7");
    $(".drilldown-title").text(GROUP_NAME+" - "+type+" Compliances");
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();
    $(".escalation-drilldown-list .td-escalation").empty();
    showComplianceApplicabilityDrillDownRecord_headingList();
    showComplianceApplicabilityDrillDownRecord(data, type);
}

function showmorerecords(){

    var getcharttype =  chartInput.chart_type;
    // Possiblities: "compliance_status", "escalations", "not_complied", "compliance_report", "trend_chart", "applicability_status"
    if(getcharttype  == "compliance_status"){
        year = chartInput.getChartYear();
        if (year == 0) {
            year = chartInput.getCurrentYear();
        }
        var filter_type = chartInput.getFilterType();
        var filterType = filter_type.replace("_", "-");
        filterType = hyphenatedToUpperCamelCase(filterType);
        requestData = {
            "domain_ids": chartInput.getDomains(),
            "from_date": chartInput.getFromDate(),
            "to_date": chartInput.getToDate(),
            "filter_type": CS_FILTERTYPENAME,
            "filter_id": CS_FILTERTYPEID,
            "compliance_status": CS_STATUS,
            "year": year,
            "record_count": SNO
        }
        client_mirror.getComplianceStatusDrillDown(
            requestData,
            function (status, data) {
                complianceStatusDrilldown(CS_STATUS, data['drill_down_data']);
            }
        );
    }
    else if(getcharttype == "escalations"){
        ES_YEAR = chartInput.getEscalationYearDrilldown()
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
            "year": parseInt(ES_YEAR),
            "record_count": SNO
        }
        client_mirror.getEscalationDrillDown(
            requestData,
            function (status, data) {
                escalationDrilldowndelayed("delayed", data);
                escalationDrilldownnotcomplied("not_complied", data);
            }
        );

    }
    else if(getcharttype == "not_complied"){

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
            "not_complied_type": NC_TYPE,
            "record_count": SNO
        }
        client_mirror.getNotCompliedDrillDown(
            requestData,
            function (status, data) {
                notCompliedDrilldown("not_complied", data['drill_down_data']);
            }
        );

    }
    else if(getcharttype == "trend_chart"){
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
        );

    }
    else if(getcharttype == "applicability_status"){
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
            "applicability_status": CAS_TYPE,
            "record_count": SNO
        }
        client_mirror.getComplianceApplicabilityDrillDown(
            requestData,
            function (status, data) {
                if(data["drill_down_data"] == ''){
                    $("#pagination").hide();
                }
                showComplianceApplicabilityDrillDownRecord(data, CAS_TYPE);
            }
        );
    }


}
function showComplianceApplicabilityDrillDownRecord_headingList(){
    var tableHeading = $('#templates .compliance-applicable-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);
}
function showComplianceApplicabilityDrillDownRecord_level1List(data){
    if(CAS_LEVEL1 != data["level1_name"]){
        var tableLevel1 = $('#templates .compliance-applicable-status .tr-level1');
        var cloneLevel1 = tableLevel1.clone();
        $(".level-heading", cloneLevel1).html(data["level1_name"]);
        $(".table-drilldown-list").append(cloneLevel1);

        $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+ACCORDIONCOUNT+'"></tbody>');
        if(ACCORDIONCOUNT == 1){
            $('.accordion-content'+ACCORDIONCOUNT).addClass("default");
        }
        CAS_LEVEL1 = data["level1_name"];
    }

}
function showComplianceApplicabilityDrillDownRecord_unitList(data){
    if(CAS_UNITNAME != data['unit_name']){
        var tableUnit = $('#templates .compliance-applicable-status .tr-unit');
        var cloneUnit = tableUnit.clone();
        var disp_unitname = '';
        $(".heading", cloneUnit).html(data['unit_name']);
        $('.accordion-content'+ACCORDIONCOUNT).append(cloneUnit);
        CAS_UNITNAME = data['unit_name'];
    }
}
function showComplianceApplicabilityDrillDownRecord_complianceList(val){
    SNO = SNO + 1;
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

        if(sMonth != '') sMonth = getMonth_IntegettoString(sMonth);

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
    $(".sno", clone).html(SNO);
    $(".statutory-name", clone).html(val["statutory_provision"]);
    var download_url = val["download_url"];
    if(download_url == null){
        $(".compliance-task-name", clone).html(val["compliance_task"])
    }else{
        $('.compliance-task-name', clone).html('<a href= "'+ download_url +'" target="_new">'+val["compliance_task"]+'</a>');
    }
    $(".compliance-description-name", clone).html('<abbr class="page-load" title="'+cDescription+'">'+partDescription+'</abbr>');
    $(".penal-consequences-name", clone).html('<abbr class="page-load" title="'+cPenalConsequences+'">'+partPenalConsequences+'</abbr>');
    $(".compliance-frequency-name", clone).html(frequency);
    $(".repeats", clone).html(statutorydate);
    //$(".statutory-date", clone).html(statutorydate);
    $(".trigger-before", clone).html(triggerbefore);
    $('.accordion-content'+ACCORDIONCOUNT).append(clone);

}

function showComplianceApplicabilityDrillDownRecord(data, type){

    FULLARRAYLIST = [];
    var data =  data['drill_down_data'];

    $.each(data, function(i, val){
        var level1_Object = new Object();
        level1_Object.level1_name = val['level1_statutory_name'];
        var list_comp = val["compliances"]
        FULLARRAYLIST.push(level1_Object);

        $.each(list_comp, function(i1, val1){
            var unit_Object = new Object();
            unit_Object.unit_name = i1;

            var list_compliancesDetails = val1;
            delete val1;
            FULLARRAYLIST.push(unit_Object);

            $.each(list_compliancesDetails, function(i2, val2){
                FULLARRAYLIST.push(val2);
            });
        });
    });

    var totallist = FULLARRAYLIST.length;
    // if(totallist > PAGESIZE){
    //     $('#pagination').show();
    // }
    // else{
    //     $('#pagination').hide();
    // }
    //var sub_array_list = get_sub_array(FULLARRAYLIST, STARTCOUNT, ENDCOUNT);

    for(var y = 0;  y < totallist; y++){
            if(Object.keys(FULLARRAYLIST[y])[0] == "level1_name"){
                ACCORDIONCOUNT++;
                showComplianceApplicabilityDrillDownRecord_level1List(FULLARRAYLIST[y]);
            }
            else if(Object.keys(FULLARRAYLIST[y])[0] == "unit_name"){
                showComplianceApplicabilityDrillDownRecord_unitList(FULLARRAYLIST[y]);
            }
            else if(Object.keys(FULLARRAYLIST[y])[0] == "description"){
                showComplianceApplicabilityDrillDownRecord_complianceList(FULLARRAYLIST[y]);
            }
    }
    accordianType('accordion', 'accordion-toggle', 'accordion-content');
}

// function accordianType(idtype, toggleClass, contentClass){
//     $('#'+idtype).find('.'+toggleClass).click(function(){
//         $(this).next().slideToggle('fast');
//         $("."+contentClass).not($(this).next()).slideUp('fast');
//     });
// }

function showNotCompliedDrillDownRecord(data){
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();
    $(".escalation-drilldown-list .td-escalation").empty();
    $(".drilldown-title").text("Over due compliances of "+GROUP_NAME);

    var tableHeading = $('#templates .notComplied-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);

    var tableFilter = $('#templates .notComplied-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-thead-drilldown-list").append(cloneFilter);

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
    if(data == ''){
        $("#pagination").hide();
    }

    $.each(data, function(key, value){

        if(NC_UNITNAME != value["unit_name"]){
            ACCORDIONCOUNT = ACCORDIONCOUNT + 1;
            var tableUnit = $('#templates .notComplied-status .tr-unit');
            var cloneUnit = tableUnit.clone();
            $(".unit-heading", cloneUnit).html(value["unit_name"]);
            $(".table-drilldown-list").append(cloneUnit);
            $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+ACCORDIONCOUNT+'"></tbody>');
            if(ACCORDIONCOUNT == 1){
                $('.accordion-content'+ACCORDIONCOUNT).addClass("default");
            }
            NC_UNITNAME = value["unit_name"];
        }

        var unitList = value["compliances"];

        $.each(unitList, function(ke, valu){
            if(NC_LEVEL1 != ke){
                var tableLevel1 = $('#templates .notComplied-status .tr-level1');
                var cloneLevel1 = tableLevel1.clone();
                $(".heading", cloneLevel1).html(ke);
                $('.accordion-content'+ACCORDIONCOUNT).append(cloneLevel1);
                NC_LEVEL1= ke;
            }
            $.each(valu, function(k, val){
                SNO = SNO + 1;
                var tableRow = $('#templates .notComplied-status .table-row-list');
                var clone = tableRow.clone();
                $(".sno", clone).html(SNO);
                $(".businessgroup-name", clone).html(value["business_group"]);
                $(".legalentity-name", clone).html(value["legal_entity"])
                $(".division-name", clone).html(value["division"]);
                $(".industry-type-name", clone).html(value["industry_name"]);
                $(".compliance-name span", clone).html(val['compliance_name']);
                $(".assigned-to", clone).html(val['assignee_name']);
                $(".over-due", clone).html(val['ageing']);
                $('.accordion-content'+ACCORDIONCOUNT).append(clone);


            });
        });

    });
    accordianType('accordion', 'accordion-toggle', 'accordion-content');
    $('.js-filtertable').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter');
    });

}

function showEscalationDrillDownRecord(data, year){

    var filter_type = chartInput.getFilterType();
    $(".table-thead-drilldown-list").empty();
    $(".table-drilldown-list tbody").remove();
    $(".escalation-drilldown-list .td-escalation").empty();
    $('.drilldown-title').text("Escalations of "+GROUP_NAME+" for the year "+year);
    if(filter_type == "group"){
        groupWiseEscalationDrillDown("delayed", data);
        groupWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "business_group"){
        businessgroupWiseEscalationDrillDown("delayed", data);
        businessgroupWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "legal_entity"){
        legalentityWiseEscalationDrillDown("delayed", data);
        legalentityWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "division"){
        divisionWiseEscalationDrillDown("delayed", data);
        divisionWiseEscalationDrillDown("not_complied", data);
    }
    if(filter_type == "unit"){
        unitWiseEscalationDrillDown("delayed", data);
        unitWiseEscalationDrillDown("not_complied", data);
    }
    //$(".td-escalation").empty();
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
       //var status = "Not Complied"
    }
    else if (status == "delayed") {
        $(".tr-level1 th").attr("colspan", "5");
        $(".tr-unit .unit-heading").attr("colspan", "4");
        $(".delayed-by-row").show();
        $(".over-due-row").hide();
        //var status = "Delayed"
    }
    escalationDrilldown(status, data);
}
function escalationDrilldown(status, data){
    if(status == "not_complied"){
        if(ES_NC_COUNT == 1){
            $(".escalation-drilldown-list .td-escalation").append('<table class="inner-table-notcomplied-escalation-list js-filtertable_not_c"  id="accordionNC"><thead class="thead-itncel"></thead></table>');
            var h2heading = $('#templates .escalation-status .tr-h2');
            var cloneh2 = h2heading.clone();
            $(".escalation-status-value", cloneh2).css({ 'margin-top': '40px' });
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
            ES_NC_COUNT++;
        }
        escalationDrilldownnotcomplied("not_complied", data);
    }
    if(status == "delayed"){
        if(ES_D_COUNT ==1){
            $(".escalation-drilldown-list .td-escalation").append('<table class="inner-table-delayed-escalation-list js-filtertable_delayed" id="accordionD"><thead-itdel class="thead-itdel"></thead></table>');
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
            ES_D_COUNT++;
        }
        escalationDrilldowndelayed("delayed", data);
    }

}
function escalationDrilldownnotcomplied(status, data){
    if(data[status] == ''){
        $("#pagination").hide();
    }
    else{
        $("#pagination").show();
    }
    if(typeof data[status] != "undefined"){
        $.each(data[status], function(key, value){
            if(ES_NC_UNITNAME != value["unit_name"]){
                ACCORDIONCOUNTNC = ACCORDIONCOUNTNC + 1;
                var tableUnit = $('#templates .escalation-status .tr-unit');
                var cloneUnit = tableUnit.clone();
                $(".unit-heading", cloneUnit).html(value["unit_name"]);
                $(".inner-table-notcomplied-escalation-list").append(cloneUnit);
                $('.inner-table-notcomplied-escalation-list').append('<tbody class="accordion-content accordion-nc-content'+ACCORDIONCOUNTNC+'"></tbody>');
                if(ACCORDIONCOUNTNC == 1){
                    $('.accordion-nc-content'+ACCORDIONCOUNTNC).addClass("default");
                }
                ES_NC_UNITNAME = value["unit_name"];
            }
            var unitList = value["compliances"];

            $.each(unitList, function(ke, valu){
                if(ES_NC_LEVEL1 != ke){
                    var tableLevel1 = $('#templates .escalation-status .tr-level1');
                    var cloneLevel1 = tableLevel1.clone();
                    $(".heading", cloneLevel1).html(ke);
                    $('.accordion-nc-content'+ACCORDIONCOUNTNC).append(cloneLevel1);
                    ES_NC_LEVEL1 = ke;
                }
                $.each(valu, function(k, val){
                    SNO = SNO + 1;
                    var tableRow = $('#templates .escalation-status .table-row-list');
                    var clone = tableRow.clone();
                    $(".sno", clone).html(SNO);
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
                    $('.accordion-nc-content'+ACCORDIONCOUNTNC).append(clone);
                });
            });

        });

    }
    // else{
    //     var tableRow = $('#templates .escalation-status .norecords-list');
    //     var clone = tableRow.clone();
    //     $('.norecord', clone).html("No Record Found");
    //     $('.inner-table-notcomplied-escalation-list').append(clone);
    // }
    accordianTypenotcomplied('accordionNC', 'accordion-toggle', 'accordion-nc-content');
    $('.js-filtertable_not_c').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter_not_c');
    });

}
function escalationDrilldowndelayed(status, data){
    if(data[status] == ''){
        $("#pagination").hide();
    }
    else{
        $("#pagination").show();
    }
    if(typeof data[status] != "undefined"){
        $.each(data[status], function(key, value){
            if(ES_D_UNITNAME != value["unit_name"]){
                ACCORDIONCOUNTD = ACCORDIONCOUNTD + 1;
                var tableUnit = $('#templates .escalation-status .tr-unit');
                var cloneUnit = tableUnit.clone();
                $(".unit-heading", cloneUnit).html(value["unit_name"]);
                $(".inner-table-delayed-escalation-list").append(cloneUnit);
                $('.inner-table-delayed-escalation-list').append('<tbody class="accordion-content accordion-delayed-content'+ACCORDIONCOUNTD+'"></tbody>');
                if(ACCORDIONCOUNTD == 1){
                    $('.accordion-delayed-content'+ACCORDIONCOUNTD).addClass("default");
                }
                ES_D_UNITNAME = value["unit_name"];
            }
            var unitList = value["compliances"];

            $.each(unitList, function(ke, valu){
                if(ES_D_LEVEL1 != ke){

                    var tableLevel1 = $('#templates .escalation-status .tr-level1');
                    var cloneLevel1 = tableLevel1.clone();
                    $(".heading", cloneLevel1).html(ke);
                    $('.accordion-delayed-content'+ACCORDIONCOUNTD).append(cloneLevel1);
                    ES_D_LEVEL1 = ke;
                }
                $.each(valu, function(k, val){
                    SNO = SNO + 1;
                    var tableRow = $('#templates .escalation-status .table-row-list');
                    var clone = tableRow.clone();
                    $(".sno", clone).html(SNO);
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
                    $('.accordion-delayed-content'+ACCORDIONCOUNTD).append(clone);
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
    accordianTypedelayed('accordionD', 'accordion-toggle', 'accordion-delayed-content');
    $('.js-filtertable_delayed').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter_delayed');
    });

}
function accordianTypedelayed(idtype, toggleClass, contentClass){
    $('#'+idtype).find('.'+toggleClass).click(function(){
        $(this).next().slideToggle('fast');
        $("."+contentClass).not($(this).next()).slideUp('fast');
     });
}
function accordianTypenotcomplied(idtype, toggleClass, contentClass){
    $('#'+idtype).find('.'+toggleClass).click(function(){
        $(this).next().slideToggle('fast');
        $("."+contentClass).not($(this).next()).slideUp('fast');
     });
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

    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-thead-drilldown-list").append(cloneFilter);

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

    $.each(data, function(key, value){
        if(TC_UNIT != value["unit_name"]){
            ACCORDIONCOUNT = ACCORDIONCOUNT + 1;
            var tableUnit = $('#templates .compliance-status .tr-unit');
            var cloneUnit = tableUnit.clone();
            $(".unit-heading", cloneUnit).html(value["unit_name"]);
            $(".table-drilldown-list").append(cloneUnit);
            $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+ACCORDIONCOUNT+'"></tbody>');
            if(ACCORDIONCOUNT == 1){
                $('.accordion-content'+ACCORDIONCOUNT).addClass("default");
            }

            TC_UNIT = value["unit_name"];
        }
        var unitList = value["compliances"];
        $.each(unitList, function(ke, valu){
            if(TC_LEVEL1 != ke){
                var tableLevel1 = $('#templates .compliance-status .tr-level1');
                var cloneLevel1 = tableLevel1.clone();
                $(".heading", cloneLevel1).html(ke);
                $('.accordion-content'+ACCORDIONCOUNT).append(cloneLevel1);
                TC_LEVEL1 = ke;
            }
            $.each(valu, function(k, val){
                SNO = SNO + 1;
                var tableRow = $('#templates .compliance-status .table-row-list');
                var clone = tableRow.clone();
                $(".sno", clone).html(SNO);
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
                $('.accordion-content'+ACCORDIONCOUNT).append(clone);

            });
        });

    });

    accordianType('accordion', 'accordion-toggle', 'accordion-content');
    $('.js-filtertable').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter');
    });
}


function showDrillDownRecord(status, data, filterTypeName){
    //$("#pagination").hide();
    //clear escalation data
    $(".escalation-drilldown-list .td-escalation").empty();
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
    var tableHeading = $('#templates .compliance-status .tr-heading');
    var cloneHeading = tableHeading.clone();
    $(".table-thead-drilldown-list").append(cloneHeading);
    var tableFilter = $('#templates .compliance-status .tr-filter');
    var cloneFilter = tableFilter.clone();
    $(".table-thead-drilldown-list").append(cloneFilter);
    $('.drilldown-title').text(drilldownTitleText);
}

function groupWiseComplianceDrillDown(status, data){

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
    if(data == ''){
        $("#pagination").hide();
    }

    $.each(data, function(key, value){
        if(CS_LAST_UNITNAME != value["unit_name"]){
            ACCORDIONCOUNT = ACCORDIONCOUNT + 1;
            var tableUnit = $('#templates .compliance-status .tr-unit');
            var cloneUnit = tableUnit.clone();
            $(".unit-heading", cloneUnit).html(value["unit_name"]);
            $(".table-drilldown-list").append(cloneUnit);
            $('.table-drilldown-list').append('<tbody class="accordion-content accordion-content'+ACCORDIONCOUNT+'"></tbody>');
            if(ACCORDIONCOUNT == 1){
                $('.accordion-content'+ACCORDIONCOUNT).addClass("default");
            }
            CS_LAST_UNITNAME = value["unit_name"];
        }

        var unitList = value["compliances"];
        $.each(unitList, function(ke, valu){
            if(CS_LAST_LEVEL1 != ke){
                var tableLevel1 = $('#templates .compliance-status .tr-level1');
                var cloneLevel1 = tableLevel1.clone();
                $(".heading", cloneLevel1).html(ke);
                $('.accordion-content'+ACCORDIONCOUNT).append(cloneLevel1);
                CS_LAST_LEVEL1 = ke;
            }
            $.each(valu, function(k, val){
                SNO = SNO + 1;
                var tableRow = $('#templates .compliance-status .table-row-list');
                var clone = tableRow.clone();
                $(".sno", clone).html(SNO);
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
                $('.accordion-content'+ACCORDIONCOUNT).append(clone);
            });
        });

    });

    accordianType('accordion', 'accordion-toggle', 'accordion-content');
    $('.js-filtertable').on('keyup', function () {
        $(this).filtertable().addFilter('.js-filter');
    });
}
//-----------------------------------End Compliance Status--------------------------------------------------------------

function accordianType(idtype, toggleClass, contentClass){
    $('#'+idtype).find('.'+toggleClass).stop().slideDown('fast');
    $('#'+idtype).find('.'+toggleClass).click(function(e){
        e.preventDefault();
        e.stopPropagation();
        $(this).next().slideDown('fast');
        $("."+contentClass).not($(this).next()).slideUp('fast');
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
        displayMessage(message.country_required);
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
    displayLoader();
    client_mirror.getAssigneewiseComplianes(
        parseInt(country), businessgroupid, legalentityid,
        divisionid, unitid, userid,
        function (status, data) {
            updateAssigneeWiseComplianceList(data['chart_data']);
            hideLoader();
        }
    );

}

function updateAssigneeWiseComplianceList(data){
    $('.tbody-assignee-wise-compliance-list tr').remove();
    $('.compliance-details-drilldown tr').remove();
    $(".table-assignee-wise-compliance-list").show();
    $('#pagination-assignee').hide();
    $('.compliance_count_assignee').text('');
    var aSno = 0;

    var country_assignee = parseInt($("#country").val().trim());
    $.each(data, function(key, value) {
        var tableRowHeadingth = $('#templates .assignee-wise-compliance-list .unitHeading');
        var cloneHeadingth = tableRowHeadingth.clone();
        $('.unit-name', cloneHeadingth).text(value['unit_name']);
        $('.tbody-assignee-wise-compliance-list').append(cloneHeadingth);

        var assigneewiselist = value['assignee_wise_details'];
        $.each(assigneewiselist, function(ke, valu) {
            var tableRow = $('#templates .assignee-wise-compliance-list .userHeading ');
            var clone = tableRow.clone();
            var name_assignee = valu['assignee_name'];
            $('.assignee-name-for-popup', clone).html(name_assignee);
            $(clone, ".assignee-name-for-popup").on("click", function(e){
                $("#popup-year").show();
                showPopup(country_assignee, value['unit_id'], valu['user_id'], valu['assignee_name']);
            });
            $('.tbody-assignee-wise-compliance-list').append(clone);

            var list = valu['domain_wise_details'];
            $.each(list, function(k, val){
                var domainArr = [];
                var tableRowvalues = $('#templates .assignee-wise-compliance-list .assignee-row-list');
                var cloneval = tableRowvalues.clone();
                aSno++;
                $('.sno', cloneval).text(aSno);
                $('.level1value', cloneval).html(val['domain_name']);
                $('.total-count', cloneval).html(val['total_compliances']);
                $('.complied-count', cloneval).html(val['complied_count']);
                if(val['reassigned_count'] == 0){
                    $('.delayed-count', cloneval).html(val['assigned_count']);
                    $(".delayed-count", cloneval).on("click", function(e){
                        $("#popup-reassigned").show();
                    });
                }
                else{
                    var delayvalue = val['assigned_count']+" (+"+val['reassigned_count']+")";
                    $('.delayed-count', cloneval).html(delayvalue);
                    $('.delayed-count', cloneval).addClass("delayedvalue");
                    $(".delayedvalue", cloneval).on("click", function(e){
                        $("#popup-reassigned").show();
                        showPopupCompDelayed(country_assignee, value['unit_id'], valu['user_id'], val['domain_id'], valu['assignee_name']);
                    });
                }

                $('.inprogress-count', cloneval).html(val['inprogress_compliance_count']);
                $('.not-complied-count', cloneval).html(val['not_complied_count']);
                var year = null;
                $(".open-details-list", cloneval).on("click", function(e){
                    updateComplianceList(country_assignee, valu['user_id'], val['domain_id'], year, value['unit_id'],  0, valu['assignee_name'], val['domain_name']);
                });
                $('.tbody-assignee-wise-compliance-list').append(cloneval);
            });
        });

    });

}


function updateComplianceList(country_id, user_id, domain_id, year, unit_id, start_count, assigneename, domain_name){
    displayLoader();
    $('.popupoverlay').css("visibility","hidden");
    $('.popupoverlay').css("opacity","0");
    $(".table-assignee-wise-compliance-list").hide();
    $(".grid-table-dash1").show();
    snoAssignee = 0;
    $('.tbody-assignee-wise-compliance-list tr').remove();
    $('.compliance-details-drilldown tr').remove();
    $(".table-assignee-wise-compliance-list").show();
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

    if(domain_name != null && domain_name != 'null') dispDomain = domain_name;
    if(year != null && year != 'null') dispYear = year;

    $('.comp-list-year', cloneHeadingth).text(dispYear);
    $('.comp-list-domain', cloneHeadingth).text(dispDomain);

    $('.compliance-details-drilldown').append(cloneHeadingth);

    client_mirror.getAssigneewiseCompliancesDrilldown(
       country_id, user_id, domain_id, year, unit_id, start_count,
        function (status, data) {
            listingCompliance(data, userid, year);
            hideLoader();
        }
    );
}

function getShowmoreData(){
    var country = parseInt($("#country").val().trim());
    var a_user = parseInt($("#a_user").val().trim());
    var a_domain = parseInt($("#a_domain").val().trim());
    var a_year = parseInt($("#a_year").val().trim());
    var a_unit = parseInt($("#a_unit").val().trim());

    client_mirror.getAssigneewiseCompliancesDrilldown(
       country, a_user, a_domain, a_year, a_unit, snoAssignee,
        function (status, data) {
            listingCompliance(data, a_user, a_year);
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

function fullnamestatus(val){
    var fullname = null;
    if(val == "not_complied"){
        fullname = "Not Complied"
    }
    else if(val == "inprogress"){
        fullname = "Inprogress"
    }
    else if(val == "delayed"){
        fullname = "Delayed"
    }
    else if(val == "complied"){
        fullname = "Complied"
    }
    return fullname;
}

function listingCompliance(data, userid, year){
        totalRecordAssignee = data['total_count'];
        if(snoAssignee == 0){

        }
        var fullStatus = '';
        var statuswiselist = data['drill_down_data'];
        $.each(statuswiselist, function(ke, valu) {
            if(Object.keys(valu).length > 0){
                fullStatus = fullnamestatus(ke);
                if(lastStatus != fullStatus){
                    var tableRow = $('#templates .compliance-details-list .comp-list-statusheading ');
                    var clone = tableRow.clone();
                    $('.comp-list-status', clone).html(fullStatus);
                    $('.compliance-details-drilldown').append(clone);

                    var tableRowheading = $('#templates .compliance-details-list .comp-list-heading');
                    var cloneHeading = tableRowheading.clone();
                    $('.compliance-details-drilldown').append(cloneHeading);
                    lastStatus = fullStatus;
                }
            }
            var list = valu;
            $.each(list, function(k, val){
                if(lastAct != k){
                    var tableRowLevel1 = $('#templates .compliance-details-list .comp-list-level1');
                    var cloneLevel1 = tableRowLevel1.clone();
                    $(".comp-list-level1-val", cloneLevel1).text(k)
                    $(".compliance-details-drilldown").append(cloneLevel1);
                    lastAct = k;
                }
                $.each(val, function(k2, v2){
                    var tableRowvalues = $('#templates .compliance-details-list .comp-list-tablerowlist');
                    var cloneval = tableRowvalues.clone();
                    snoAssignee++;
                    var cDate = '';
                    if(v2['completion_date'] != null) cDate = v2['completion_date'];
                    $('.comp-list-sno', cloneval).text(snoAssignee);
                    $('.comp-list-compliance', cloneval).html(v2['compliance_name']);
                    $('.comp-list-startdate', cloneval).text(v2['assigned_date']);
                    $('.comp-list-duedate', cloneval).text(v2['due_date']);
                    $('.comp-list-completiondate', cloneval).text(cDate);
                    $('.compliance-details-drilldown').append(cloneval);
                });
            });
        });
        if(totalRecordAssignee == 0){
            $('#pagination-assignee').hide();
            $('.compliance_count_assignee').text('');
        }else{
            $('.compliance_count_assignee').text("Showing " + 1 + " to " + snoAssignee + " of " + totalRecordAssignee);
            if(snoAssignee >= totalRecordAssignee){
              $('#pagination-assignee').hide();
            }else{
              $('#pagination-assignee').show();
            }
        }
}


function showPopup(country_assignee, unit_assignee, user_assignee, name_assignee){
    $(".tbody-popup-list tr").remove();
    $('.popupoverlay').css("visibility","visible");
    $('.popupoverlay').css("opacity","1");
    $('.year-heading').text(name_assignee);
    window.scrollTo(0, 0);

    var popupsno = 0;
    client_mirror.getAssigneewiseYearwiseComplianes( country_assignee, unit_assignee, user_assignee,
    function (error, response) {
        if (error == null){
            if(popupsno == 0){
                var yearWiseDetails = response["chart_data"];
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
                        updateComplianceList(country_assignee, user_assignee, null, parseInt(val['year']), unit_assignee,  0, name_assignee, null);
                    });
                    $('.tbody-popup-list').append(cloneval);
                });
            }
        }
        else {
            console.log(error);
        }
      }
    );
    $('.close').click(function(){
      $('.popupoverlay').css("visibility","hidden");
      $('.popupoverlay').css("opacity","0");
    });
}
function showPopupCompDelayed(country_id, unit_id, user_id, domain_id, name_assignee){
    $(".tbody-popup-reassigned-list tr").remove();
    $('.popupoverlay1').css("visibility","visible");
    $('.popupoverlay1').css("opacity","1");
    $('.comp-delayed-heading').text(name_assignee);
    window.scrollTo(0, 0);

    var popupdelayedsno = 0;
    client_mirror.getAssigneewiseReassignedComplianes( country_id, unit_id, user_id, domain_id,
    function (error, response) {
        if (error == null){
            if(popupdelayedsno == 0){
                var reassignedlist = response["chart_data"];
                $.each(reassignedlist, function(k, val){
                    //alert('k')
                    var tableRow = $('#templates .comp-list-delayed-row-list');
                    var cloneval = tableRow.clone();
                    popupdelayedsno = popupdelayedsno + 1;
                    $('.comp-delayed-sno', cloneval).text(popupdelayedsno);
                    $('.comp-delayed-compliance', cloneval).html(val['compliance_name']);
                    $('.comp-delayed-reassigned-from', cloneval).html(val['reassigned_from']);
                    $('.comp-delayed-startdate', cloneval).html(val['start_date']);
                    $('.comp-delayed-duedate', cloneval).html(val['due_date']);
                    $('.comp-delayed-reassigned-date', cloneval).html(val['reassigned_date']);
                    $('.comp-delayed-completed-date', cloneval).html(val['completed_date']);
                    $('.tbody-popup-reassigned-list').append(cloneval);
                });
            }
        }
        else {
            console.log(error);
        }
    });

    $('.close').click(function(){
      $('.popupoverlay1').css("visibility","hidden");
      $('.popupoverlay1').css("opacity","0");
    });
}

//drilldown load function

function loadComplianceStatusDrillDown(compliance_status, filter_type_id, filter_type_name) {
    $("#pagination").show();
    $(".table-drilldown-list thead").empty();
    $(".table-drilldown-list tbody").remove();

    $(".btn-bar-chart").hide();
    $(".btn-pie-chart").hide();

    CS_STATUS = null;
    CS_FILTERTYPEID = null;
    CS_FILTERTYPENAME = null;
    CS_LAST_UNITNAME = null;
    CS_LAST_LEVEL1 = null;

    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);

    CS_STATUS = compliance_status;
    CS_FILTERTYPEID = filter_type_id;
    CS_FILTERTYPENAME = filterType;
    SNO = 0;
    ACCORDIONCOUNT = 0;
    if (chartInput.getChartYear() == 0)
        year = chartInput.getCurrentYear();
    else
        year = chartInput.getChartYear();


    requestData = {
        "domain_ids": chartInput.getDomains(),
        "from_date": chartInput.getFromDate(),
        "to_date": chartInput.getToDate(),
        "filter_type": filterType,
        "filter_id": filter_type_id,
        "compliance_status": compliance_status,
        "year": year,
        "record_count": SNO
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

    $("#pagination").show();
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
        "year": parseInt(year),
        "record_count": 0
    }
    $(".btn-back").on("click", function() {
        loadEscalationChart();
    });
    client_mirror.getEscalationDrillDown(
        requestData,
        function (status, data) {
            ESCALATION_STATUS_DRILL_DOWN_DATA = data;
            updateEscalationDrillDown(data, year);
            chartInput.setEscalationYearDrilldown = year;
        }
    );
}

function loadTrendChartDrillDown(year){
    SNO = 0;
    var filter_type = chartInput.getFilterType();
    var filterType = filter_type.replace("_", "-");
    filterType = hyphenatedToUpperCamelCase(filterType);
    var requestData = {
        "country_ids": chartInput.getCountries(),
        "domain_ids": chartInput.getDomains(),
        "filter_type": filterType,
        "filter_ids": [1],
        "year": parseInt(year),
        "record_count": SNO
    };
    $(".btn-back").on("click", function() {
        loadTrendChart();
    });
    client_mirror.getTrendChartDrillDown(
        requestData, function(status, data) {
            TREND_CHART_DATA = data;
            updateTrendChartDrillDown(status, data, year);
        }
    );
}

function loadNotCompliedDrillDown(type){
    SNO = 0;
    NC_TYPE = null;
    NC_UNITNAME = null;
    NC_LEVEL1 = null;
    NC_TYPE = type;
    ACCORDIONCOUNT = 0;

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
        "not_complied_type": type,
        "record_count": SNO
    }
    client_mirror.getNotCompliedDrillDown(
        requestData,
        function (status, data) {
            NOT_COMPLIED_DRILL_DOWN_DATA = data;
            updateNotCompliedDrillDown(status, data);
        }
    );
}

function loadComplianceApplicabilityDrillDown(type){
    CAS_TYPE = null;
    CAS_LEVEL1 = null;
    CAS_UNITNAME = null;
    SNO = 0;
    $("#pagination").show();

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
        "applicability_status": type,
        "record_count": SNO
    }
    CAS_TYPE = type;
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
        loadCharts();
    });
}

function initializeCharts () {
    initializeFilters();
    initializeChartTabs();
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
        get_notification_count();
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

